'''
Created on 25 May 2020

@Author: Jagadeesh LakshmiNarasimhan
'''
import spacy
import re
from jira.client import JIRA, JIRAError


class FormQuery:
    '''
    This class contain forming of query related methods
    '''
    def __init__(self):
        self.and_val = ' AND '
        self.or_val = ' OR '

    def set_assignee(self, value, query):
        '''set_assignee is method of FormQuery

        on forming of jira query, assignee of the ticket will be added to the query.
        :param value: name of the assignee
        :param query: jira search query
        :return: search query with added assignee to it.
        '''
        if query == '':
            query = 'assignee in ({})'.format(value)
        else:
            query = query + self.and_val + 'assignee in ({})'.format(value)
        return query

    def set_text(self, value, query):
        '''set_value is method of FormQuery

        on forming of jira query, text element for the searching will be added to the query.
        :param value: set of string to be searched
        :param query: jira search query
        :return: search query with added search text to it.
        '''
        # "project = ARM AND resolution = Unresolved AND labels = ATM AND assignee in (jagdeeshlaks) ORDER BY priority DESC"
        # 'text ~ "abc"'
        flag = 1
        for noun in value:
            if flag:
                query = "(" + query
                flag = None
            if query == '(':
                query = query + 'text ~ "{}"'.format(noun)
            else:
                query = query + self.or_val + 'text ~ "{}"'.format(noun)
        if not flag:
            query = query + ")"
        return query

    def set_component(self, value, query):
        '''set_component is method of FormQuery

        on forming of jira query, component for the ticket will be added to the query.
        :param value: component of the ticket
        :param query: jira search query
        :return: search query with added component to it.
        '''
        for component in value:
            if query == '':
                query = 'component = {}'.format(component)
            else:
                query = query + self.and_val + 'component = "{}"'.format(component)
        return query

    def set_label(self, value, query):
        '''set_label is method of FormQuery

        on forming of jira query, label for the ticket will be added to the query.
        :param value: label of the ticket
        :param query: jira search query
        :return: search query with added label to it.
        '''
        for pos in range(len(value)):
            if pos == 0:
                if query == '':
                    query = '(labels = "{}"'.format(value[pos])
                else:
                    query = query + self.and_val + '(labels = "{}"'.format(value[pos])
            else:
                query = query + self.or_val + 'labels = "{}"'.format(value[pos])
        if len(value) >= 1:
            query = query + ")"

        return query

    def set_project(self, value, query):
        '''set_label is method of FormQuery

        on forming of jira query, project for the ticket will be added to the query.
        :param value: project name of the ticket
        :param query: jira search query
        :return: search query with added project name to it.
        '''
        if query == '':
            query = 'project = {}'.format(value)
        else:
            query = query + self.and_val + 'project = {}'.format(value)
        return query

class Tracker:
    '''
    This class contain fetching infomation from jira and updating the results in the jira ID.
    '''
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.final_words_unique = ''

    def get_issue(self, jira, issue_id):
        '''get_issue is method of Tracker

        This method will get all the information about the given jira ticket
        :param jira: instance of jira
        :param issue_id: jira ticket
        :return: Dictionary will be returned with all the information of the given ticket.
        '''
        x = jira.issue(issue_id)
        URL = x.fields.status.iconUrl
        URL_append = r'browse/' + issue_id
        try:
            assignee_name = x.fields.assignee.name
        except:
            assignee_name = x.fields.assignee.accountId
        component = []
        for field in (x.fields.components):
             component.append(field.name)
        labels = (x.fields.labels)
        if (x.fields.description) == None:
            search_stuff = x.fields.summary
        elif x.fields.summary in x.fields.description:
            search_stuff = x.fields.description
        else:
            search_stuff = x.fields.summary + '\n' + x.fields.description
        search_stuff = search_stuff.lower()
        highlighted_word = (re.findall(r'\[(.+?)\]', search_stuff))
        search_stuff = re.sub(r"[^a-zA-Z0-9]+", ' ', search_stuff).strip()
        doc = self.nlp(search_stuff)

        # Analyze syntax
        noun_phrase = [chunk.text.lower() for chunk in doc.noun_chunks]

        # Find named entities, phrases and concepts
        list_items = []
        for entity in doc.ents:
            if entity.label_ == 'DATE':
                list_items.append(entity.text.lower())
        final_words = (list(filter(lambda item: item not in list_items, noun_phrase)))
        final_words.extend(highlighted_word)
        self.final_words_unique = list(set(final_words))
        dict_value = {"search": self.final_words_unique,
                      'assignee': assignee_name,
                      'components': component,
                      'labels': labels,
                      'project': x.fields.project.key,
                      'URL': URL + URL_append,
                      'task_id': x.key
                      }
        return dict_value

    def get_query(self, jira, input):
        '''get_query is method of Tracker

        This method will form query on basis of input result from get_issue method.
        :param jira: instance of jira
        :param input: Dictionary(output of get_issue method) of jira information
        :return: well formed jira search query
        '''
        query = ''
        mapper = {'search': FormQuery().set_text,
                  'assignee': FormQuery().set_assignee,
                  'components': FormQuery().set_component,
                  'labels': FormQuery().set_label,
                  'project': FormQuery().set_project}
        for key, value in input.items():
            if key in mapper:
                query = mapper[key](value, query)
        query = query + " AND issuetype = Bug"
        return query

    def search_mode(self, jira, query):
        '''search_mode is method of Tracker

        This method will execute the query and get the results in list format.
        :param jira: instance of jira
        :param query: jira search query
        :return: list of bug from the search query.
        '''
        x = jira.search_issues(query)
        bug_list = []
        for each in x:
            bug_list.append(each.raw['key'])
        return bug_list

    def create_issue(self, jira, bug_list, input_value, description):
        '''create_issue is method of Tracker

        This method will create an issue in the given ticket as sub-task. The issue will contain all the related bugs from the assignee.
        :param jira: instance of jira
        :param bug_list: an output from the filter_issue method.
        :param input_value: dictionary of jira objects
        :param description: an additional note added to the description under "Added Note"
        '''
        projects = jira.projects()
        keys = [project for project in projects]
        issue_dict = {
            'project': {'key': input_value['project']},
            'summary': 'Please make sure this as Prerequisites for dev-test',
            'description': 'This {} is your previous bug fix in this components, please make sure this issue is not rendering in your current fix \n {} \n Added Note: \n \n {}'.format(bug_list, input_value['URL'], description),
            'issuetype': {'name': 'Sub-task'},
            'assignee': {'name': input_value['assignee']},
            'parent': {'key': input_value['task_id']},
        }
        new_issue = jira.create_issue(fields=issue_dict)
        issue_dict['sub-task'] = new_issue.key
        return issue_dict


    def filter_issue(self, jira, item_list):
        '''filter_issue is method of Tracker

        This method will filter the set of bug by match the most content using NLP(spacy-python package).
        :param jira: instance of jira
        :param item_list: an output from the search_mode method.
        :return: set of list of filtered bugs using NPL concept.
        '''
        filter_dict = {}
        for issue_id in item_list:
            x = jira.issue(issue_id)
            if (x.fields.description) == None:
                search_stuff = x.fields.summary
            elif x.fields.summary in x.fields.description:
                search_stuff = x.fields.description
            else:
                search_stuff = x.fields.summary + '\n' + x.fields.description
            search_stuff = search_stuff.lower()
            search_stuff = re.sub(r"[^a-zA-Z0-9]+", ' ', search_stuff).strip()
            filter_dict[issue_id] = [len(list(filter(lambda noun: noun in search_stuff, self.final_words_unique))), x.fields.summary]
        sorted_list = (sorted(filter_dict.items(), key=lambda kv: (kv[1][0], kv[0][0]), reverse = True))
        outpt = []
        for stuff in sorted_list:
            stuff_list = (list(stuff))
            stuff_list[1].pop(0)
            stuff_list[1] = stuff_list[1][0]
            outpt.append(stuff_list)
        return outpt

class Trigger:
    """
    This class is a initial place where it will trigger the script.
    """
    def __init__(self):
        self.obj = Tracker()
    def jira_login(self, jira_server, jira_user, jira_password):
        '''jira_login is method of Trigger

        This method will authenticate with given jira credentials
        :param jira_server: server name of the jira
        :param jira_user: username/userID of the jira
        :param jira_password: password of jira
        :return: instance of the user's jira
        '''
        # jira_server = "https://labweek.atlassian.net/"
        # jira_user = "viper.labweek@gmail.com"
        # jira_password = "ElJiEgtUqtf9JXXNqywZF0BC"

        try:
            jira_server = {'server': jira_server}
            jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))
        except JIRAError as a:
            print(a.status_code)
            raise
        return jira

    def windfall(self, ISSUE_ID, jira_session, description):
        '''windfall is a method of Trigger

        This is the master flow trigger method. This will initiate complete process of the script
        :param ISSUE_ID: jira task-ID(use case for the development)
        :param jira_session: instance of the jira
        '''
        input_value = self.obj.get_issue(jira_session, ISSUE_ID)
        query = self.obj.get_query(jira_session, input_value)
        value = self.obj.search_mode(jira_session, query)
        outpt = self.obj.filter_issue(jira_session, value)
        return (self.obj.create_issue(jira_session, value, input_value, description))
