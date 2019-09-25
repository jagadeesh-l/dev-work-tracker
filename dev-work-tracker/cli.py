import spacy
import re
from jira.client import JIRA, JIRAError


class FormQuery:
    def __init__(self):
        self.and_val = ' AND '
        self.or_val = ' OR '

    def set_assignee(self, value, query):
        if query == '':
            query = 'assignee in ({})'.format(value)
        else:
            query = query + self.and_val + 'assignee in ({})'.format(value)
        return query

    def set_text(self, value, query):
        # "project = VSM AND resolution = Unresolved AND labels = AKM AND assignee in (jagadeeshlaks) ORDER BY priority DESC"
        'text ~ "abc"'
        flag = 1
        for noun in value:
            if flag:
                print(query)
                query = "(" + query
                flag = None
                print(query)
            if query == '(':
                query = query + 'text ~ "{}"'.format(noun)
            else:
                query = query + self.or_val + 'text ~ "{}"'.format(noun)
        if not flag:
            query = query + ")"
        print(query)
        # exit()
        return query

    def set_component(self, value, query):
        for component in value:
            if query == '':
                query = 'component = {}'.format(component)
            else:
                query = query + self.and_val + 'component = "{}"'.format(component)
        return query

    def set_label(self, value, query):
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
        if query == '':
            query = 'project = {}'.format(value)
        else:
            query = query + self.and_val + 'project = {}'.format(value)
        return query

class FindIssue:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.final_words_unique = ''

    def login_check(self):
        jira_server = "https://ccp.sys.comcast.net/"
        jira_user = "Jlaksh512"
        jira_password = "Videoip!23"
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

    def get_issue(self, jira, issue_id):
        x = jira.issue(issue_id)
        # print (x.fields.description)
        # print (x.fields.summary)
        # print (x.fields.assignee.name)
        # print ("NLP")
        component = []
        for field in (x.fields.components):
             component.append(field.name)
        print(component)
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
        # print("Noun phrases:", noun_phrase)
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

        # Find named entities, phrases and concepts
        list_items = []
        for entity in doc.ents:
            print(entity.text, entity.label_)
            if entity.label_ == 'DATE':
                list_items.append(entity.text.lower())
        final_words = (list(filter(lambda item: item not in list_items, noun_phrase)))
        final_words.extend(highlighted_word)
        self.final_words_unique = list(set(final_words))
        dict_value = {"search": self.final_words_unique,
                      'assignee': x.fields.assignee.name,
                      'components': component,
                      'labels': labels,
                      'project': x.fields.project.key,
                      }
        print(dict_value)
        return dict_value

    def get_query(self, jira, input):
        query = ''
        mapper = {'search': FormQuery().set_text,
                  'assignee': FormQuery().set_assignee,
                  'components': FormQuery().set_component,
                  'labels': FormQuery().set_label,
                  'project': FormQuery().set_project}
        for key, value in input.items():
            if key in mapper:
                query = mapper[key](value, query)
                # query = return_value + query
                # print("sdfsdfs")
                # print(query)
        query = query + " AND issuetype = Bug"
        print(query)
        return query

    def search_mode(self, jira, query):
        x = jira.search_issues(query)
        bug_list = []
        for each in x:
            bug_list.append(each.raw['key'])
        return bug_list

    def create_issue(self, jira, bug_list):
        # jira_server = "https://labweek.atlassian.net/"
        # jira_user = "viper.labweek@gmail.com"
        # jira_password = "ElJiEgtUqtf9JXXNqywZF0BC"
        #
        # try:
        #     jira_server = {'server': jira_server}
        #     jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))
        # except JIRAError as a:
        #     print(a.status_code)
        #     raise
        projects = jira.projects()
        keys = [project for project in projects]
        print(keys)
        issue_dict = {
            'project': {'key': 'VSM'},
            'summary': 'Please make sure this as Prerequisites for dev-test',
            'description': 'This {} is your previous bug fix in this components, please make sure this issue is not rendering in your current fix \n https://labweek.atlassian.net/browse/VSM-7'.format(bug_list),
            'issuetype': {'name': 'Bug'},
            'assignee': {'name': 'jagadeeshlaks'},
        }
        new_issue = jira.create_issue(fields=issue_dict)
        print(new_issue)

    def filter_issue(self, jira, item_list):
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


class StartPoint:
    def master_fun(self, ISSUE_ID):
        obj = FindIssue()
        jira_session = obj.login_check()
        input_value = obj.get_issue(jira_session, ISSUE_ID)
        query = obj.get_query(jira_session, input_value)
        value = obj.search_mode(jira_session, query)
        outpt = obj.filter_issue(jira_session, value)
        print(outpt)
        # obj.create_issue(jira_session, value)

if __name__ == '__main__':
    obj = StartPoint()
    issue_id = "VIPER-4888"
    issue_id = "VIPER-4763"
    issue_id = "VIPER-4726"
    issue_id = "VIPER-4578"
    issue_id = "VIPER-4563"
    # issue_id = "VPI-1224"
    obj.master_fun(issue_id)
