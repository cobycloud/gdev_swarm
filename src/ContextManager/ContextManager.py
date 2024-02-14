from openai import OpenAI
import requests
import base64
import logging
import json
from typing import Union, List


from base64 import b64encode


token ='your-github-token'
client = OpenAI(api_key='your-api-key')

def write_files_to_github(project_name, description, token):
    try:
        create_github_repository(app_name, 'a precursor to loving monica', token)
    except:
        pass
    
    with open(f'{project_name}-files-v2.json', 'r') as f:
        file_contents = json.load(f)
    
    for path, content in file_contents.items():
        if path.startswith('/'):
            path = path[1:]
        create_or_update_file('gslcloud', app_name, path, content, 'init', token)


def save_manager_files(project_name, manager):

    with open(f'{project_name}-chat-v2.json', 'w') as f:
        json.dump(manager.responses, f, indent=4)
        
    with open(f'{project_name}-files-v2.json', 'w') as f:
        json.dump(manager.files, f, indent=4)
    
    with open(f'{project_name}-revised_files-v2.json', 'w') as f:
        json.dump(manager.revised_files, f, indent=4)



def get_github_api_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def create_github_repository(repo_name, description, token):
    headers = get_github_api_headers(token)

    data = {
        "name": repo_name,
        "private": True,
        "auto_init": True,  # Initialize the repository with a README.md file
        "description": description,
        "license_template": "mit",
    }

    create_repo_url = "https://api.github.com/user/repos"

    response = requests.post(create_repo_url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
        print(f"Repository URL: {response.json()['html_url']}")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(f"Error message: {response.text}")

def create_or_update_file(repo_owner, repo_name, file_path, file_content, commit_message, token):
    
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    print(api_url)
    headers = get_github_api_headers(token)

    # Check if the file already exists
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # File exists, get the current commit SHA
        current_sha = response.json()['sha']

        # Update the file
        data = {
            "message": commit_message,
            "content": b64encode(file_content.encode()).decode(),
            "sha": current_sha
        }
        response = requests.put(api_url, json=data, headers=headers)
    else:
        # File does not exist, create a new file
        data = {
            "message": commit_message,
            "content": b64encode(file_content.encode()).decode()
        }
        response = requests.put(api_url, json=data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print(f"File '{file_path}' added/updated successfully.")
        print(f"File URL: {response.json()['content']['html_url']}")
    else:
        print(f"Failed to add/update file. Status code: {response.status_code}")
        print(f"Error message: {response.text}")


class ContextManager:
    def __init__(self, 
                 github_token, 
                 prompt_engineer_file_path, 
                 prompt_engineer_v2_file_path, 
                 prompt_engineer_v3_file_path, 
                 solutions_architect_dev_file_path, 
                 software_dev_file_path,
                 github_dev_file_path,
                 technical_writer_file_path,
                 qa_code_reviewer_file_path,
                 project_manager_file_path):
        self.github_token = github_token
        self.contexts = {}
        self.VARS = {}
        self._add_context("Prompt Engineer", prompt_engineer_file_path)
        self._add_context("Prompt Engineer V2", prompt_engineer_v2_file_path)
        self._add_context("Prompt Engineer V3", prompt_engineer_v3_file_path)
        self._add_context("Solutions Architect", solutions_architect_dev_file_path)
        self._add_context("Software Developer", software_dev_file_path)
        self._add_context("Github Admin", github_dev_file_path)
        self._add_context("Technical Writer", technical_writer_file_path)
        self._add_context("QA Code Reviewer", qa_code_reviewer_file_path)
        self._add_context("Project Manager", project_manager_file_path)
        
        
        self.data = {}
        self.responses = []
        self.files = {}
        self.revised_files = {}
        self.project_tree = ""
        self.project_tree_raw = ""
        self.software_development_readout = ""
        
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value  # Implement item assignment
        print(f"<ContextManager> {value} stored in data[{key}]")

    def __delitem__(self, key):
        del self.data[key]  # Optionally, implement item deletion

    def __str__(self):
        return str(self.data)  # For a human-readable representation

        
    def _add_context_vars(self, role, file_path):
        try:
            with open(file_path, 'r') as file:
                context = file.read()
        except FileNotFoundError as e:
            logging.error(f"Failed to add context for {role}: {e}")
            raise
        self.VARS[role] = context

    def _add_context(self, role, file_path):
        try:
            with open(file_path, 'r') as file:
                context = file.read()
        except FileNotFoundError as e:
            logging.error(f"Failed to add context for {role}: {e}")
            raise
        self.contexts[role] = context

    def create_llm_context(self, variables):
        context = self.contexts["Prompt Engineer"]
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": variables},
        ]

        
        response = client.chat.completions.create(
          model="gpt-3.5-turbo-16k",
          messages=messages,
          temperature=1,
          max_tokens=2933,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None
        )
        result = json.loads(response.json())['choices'][0]['message']['content']
        #print(f"\n\n{result}\n\n")
        self.responses.append({"role": "Prompt Engineer", "response": result})
        return result

    def create_llm_context_v2(self, variables):
        try:
            context = self.contexts["Prompt Engineer V2"]
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": variables},
            ]

            
            response = client.chat.completions.create(
              model="gpt-3.5-turbo-16k",
              messages=messages,
              temperature=1,
              max_tokens=2933,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              stop=None
            )
            result = json.loads(response.json())['choices'][0]['message']['content']
            #print(f"\n\n{result}\n\n")
            self.responses.append({"role": "Prompt Engineer V2", "response": result})
            return result
        except Exception as e:
            print(f"create_llm_context_v2 error: {e}")

    def create_llm_context_v3(self, variables):
        try:
            context = self.contexts["Prompt Engineer V3"]
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": variables},
            ]

            
            response = client.chat.completions.create(
              model="gpt-3.5-turbo-16k",
              messages=messages,
              temperature=1,
              max_tokens=8000,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              stop=None
            )
            result = json.loads(response.json())['choices'][0]['message']['content']
            #print(f"\n\n{result}\n\n")
            self.responses.append({"role": "Prompt Engineer V3", "response": result})
            return result
        except Exception as e:
            print(f"create_llm_context_v2 error: {e}")

    def get_llm_response_from_context(self, context, conversation_flow: Union[str, None] = None, role: Union[str, None] = None):
        try:
            if conversation_flow:
                messages = [{"role": "system", "content": context}]
                for each in conversation_flow:
                    messages.append(each)
            else:
                messages = [
                    {"role": "system", "content": context},
                ]
            response = client.chat.completions.create(
              model="gpt-3.5-turbo-16k",
              messages=messages,
              temperature=1,
              max_tokens=2933,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              stop=None
            )
            result = json.loads(response.json())['choices'][0]['message']['content']
            
            if role:
                self.responses.append({"role": role, "response": result})
                #print(f"\n\n{role}:\n\t {result}\n\n")
            else:
                self.responses.append({"role": "unknown", "response": result})
                #print(f"\n\n{role}:\n\t {result}\n\n")
            return result
        except Exception as e:
            print(f"get_llm_response_from_context: {e}")

    def get_llm_response(self, role, conversation_flow: Union[str, None] = None, filename: Union[str, None] = None):
        context = self.contexts[role]
        if conversation_flow:
            messages = [{"role": "system", "content": context}]
            for each in conversation_flow:
                messages.append(each)
        else:
            messages = [
                {"role": "system", "content": context},
            ]            
        response = client.chat.completions.create(
          model="gpt-3.5-turbo-16k",
          messages=messages,
          temperature=1,
          max_tokens=2933,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None
        )
        result = json.loads(response.json())['choices'][0]['message']['content']
        self.responses.append({"role": role, "response": result})
        #print(f"\n\n{role}:\n\t {result}\n\n")
        self.parse_message_for_file({"role": role, "response": result}, filename=filename)
        return result


    def parse_message_for_file(self, message, filename: Union[str, None] = None):
        if message['role'] == 'Software Developer' or message['role'] == 'Technical Writer':
            try:
                split_list = message['response'].split('*****')
                try:
                    split_list.remove('')
                except:
                    pass
                print(split_list)
                try:
                    for x in range(0, len(split_list), 2):
                        parsed_filename = split_list[x].replace(':', '')
                        code = split_list[x+1]
                        
                        code = code.split('\n')
                        
                        start = None
                        end = None
                        
                        if '.md' not in parsed_filename:
                            
                            for count, value in enumerate(code):
                                if '```' in value:    
                                    if not start:
                                        start = count
                                    else:
                                        end = count
                            code = '\n'.join(code[start+1:end])
                                    
                        else:
                            str_array = []
                            for count, value in enumerate(code):
                                if value != ':':
                                    str_array.append(value)
                            code = '\n'.join(str_array)
                            
                        
                        if code != '' and code != ' ':
                            
                            if filename:
                                self.files.update({filename:code})
                            else:
                                self.files.update({parsed_filename:code})
                except Exception as e:
                    print(str(e))
                    print(str(e))
                    print(str(e))
                    print(str(e))
                    print(str(e))
                    print(str(e))
                    print(str(e))
                    print(str(e))
                                            
            except IndexError:
                pass
        
    def generate_role_context(self, role, goal, nongoal, product):
        VARS = f"Role:{role}\nGoal:{goal}\nNon-Goal:{nongoal}\nProduct:{product}"
        context = self.create_llm_context(VARS)
        self.contexts[role] = context
        return self.contexts[role]

    def generate_role_context_v2(self, product, 
        role, goal, nongoal, listen_to, respond_to, output, request):
        try:
            VARS = f'''Role: {role}
            Goal: {goal}
            Non-Goal: {nongoal}
            Product: {product}
            Listen To: {listen_to}
            Deliver To: {respond_to}
            Output: {output}
            Request: {request}
            '''
            context = self.create_llm_context_v2(VARS)
            self.contexts[role] = context
            return self.contexts[role]
        except Exception as e:
            print(f"generate_role_context_v2 error: {e}")

    def generate_role_context_v3(self, product, 
        role, goal, nongoal, listen_to, respond_to, output, need):
        try:
            VARS = f'''Role: {role}
            Goal: {goal}
            Non-Goal: {nongoal}
            Product: {product}
            Listen To: {listen_to}
            Deliver To: {respond_to}
            Output: {output}
            Need: {request}
            '''
            context = self.create_llm_context_v2(VARS)
            self.contexts[role] = context
            return self.contexts[role]
        except Exception as e:
            print(f"generate_role_context_v3 error: {e}")

    def generate_role_context_v4(self, role, variables):
        try:
            variable_sub_str = f'role: {role}\n'
            for each in variables:
                key = list(each.keys())[0]
                value = list(each.values())[0]
                
                variable_sub_str += f"{key}: {value}\n"

            context = self.create_llm_context_v3(variable_sub_str)
            self.contexts[role] = context
            return self.contexts[role]
        except Exception as e:
            print(f"generate_role_context_v4 error: {e}")


    def generate_role_context_from_variables(self, role, product):
        VARS = f"{self.VARS[role]} {product}"
        print(VARS)
        context = self.create_llm_context(VARS)
        self.contexts[role] = context
        return self.contexts[role]


    def generate_role_contexts(self, product):
        CEO_VARS = f"{self.VARS['CEO']} {product}"
        print(CEO_VARS)
        ceo_context = self.create_llm_context(CEO_VARS)
        self.contexts["CEO"] = ceo_context

        CPO_VARS = f"{self.VARS['CPO']} {product}"
        cpo_context = self.create_llm_context(CPO_VARS)
        self.contexts["CPO"] = cpo_context

        CTO_VARS = f"{self.VARS['CTO']} {product}"
        cto_context = self.create_llm_context(CTO_VARS)
        self.contexts["CTO"] = cto_context
        
        return self.contexts['CEO'], self.contexts['CPO'], self.contexts['CTO']
        

    def simulate_executive_conversation(self):
        kickstart = self.get_llm_response('CEO')
        kickstart = {"role": "user", "content": kickstart}
        
        cpo_first = self.get_llm_response('CPO', [kickstart])
        cpo_first_send = {"role": "user", "content": cpo_first}
        cpo_first_self = {"role": "assistant", "content": cpo_first}
        
        
        
        cto_first = self.get_llm_response('CTO', [kickstart, cpo_first_self])
        cto_first_send = {"role": "user", "content": cto_first}
        cto_first_self = {"role": "assistant", "content": cto_first}
        
        self.software_development_readout = cto_first
        
        #cpo_second = self.get_llm_response('CPO', [kickstart, cpo_first_self, cto_first_send])
        #cpo_second_send = {"role": "user", "content": cpo_second}
        
        #cto_second = self.get_llm_response('CTO', [kickstart, cpo_first_send, cto_first_self, cpo_second_send])

            
        return cto_first


    def ask_cto(self, question):
        
        
        # Now We Reset context before we get too big and add our last checkpoint
        conversation_flow = [software_development_readout_send]
        conversation_flow.append({"role": "assistant", "content": self.raw_project_tree })
        
        user_input = {"role": "user", "content": question}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to Software Development Readout."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        

        user_input = {"role": "user", "content": "Show me the complete Software Development Readout."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        
        

        self.software_development_readout = response
        return project_tree
 

    def get_project_tree_from_question_list(self, questions: List[str]):
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        
        for count, question in enumerate(questions):
            
            user_input = {"role": "user", "content": question}
            conversation_flow = [software_development_readout_send]
            conversation_flow.append(user_input)
            
            response = self.get_llm_response("Project Manager", conversation_flow)
            conversation_flow.append({"role": "user", "content": response})
            
            user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
            conversation_flow.append(user_input)
            response = self.get_llm_response("Project Manager", conversation_flow)
            conversation_flow.append({"role": "user", "content": response})
            
            
            if (count % 4 == 0 ) or (count == len(questions)-1):
                # We get final reset
                user_input = {"role": "user", "content": "Show me the complete project tree."}
                response = self.get_llm_response("Project Manager", conversation_flow)
                
                print('checkpoint:', count)
                self.raw_project_tree = response
            
            
           
            
            


        
        updated_project_tree = {"role": "user", "content": response}
        # We convert the project tree in a manner that enables the Software Development team to iterate through files during development.
        user_input = {"role": "user", 
                      "content": '''convert this into a txt file that contains all files with their full paths included.
                      example: github-repository-name/.git
                      
                      Your responses should always follow this format:
                      github-repository-name/.git
                      github-repository-name/README.md
                      
                      '''}
        self.project_tree = self.get_llm_response("Project Manager", [software_development_readout_send, 
                                                  updated_project_tree, 
                                                  user_input])
        return self.project_tree       

    def get_project_tree(self):
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        
        
        conversation_flow = [software_development_readout_send]
 
        response = self.get_llm_response("Project Manager", [software_development_readout_send])
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "How can we enhance the project tree so that it better aligns with the features in the Software Development Readout?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we handle user authentication?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we enhance our backend api to ensure we have the files we need to talk to our databases? This component is vital to the success of the platform."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we enhance our frontend api?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we enhance our frontend app?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        # We get final reset
        user_input = {"role": "user", "content": "Show me the complete project tree."}
        response = self.get_llm_response("Project Manager", conversation_flow)
        
        print('first checkpoint')
        self.raw_project_tree = response
        # Now We Reset context before we get too big
        conversation_flow = [software_development_readout_send]
        conversation_flow.append({"role": "user", "content": response})


        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we handle models and schemas?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we handle database connectors?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        # We get final reset
        user_input = {"role": "user", "content": "Show me the complete project tree."}
        response = self.get_llm_response("Project Manager", conversation_flow)
        
        print('second checkpoint')
        self.raw_project_tree = response
        
        # Now We Reset context before we get too big
        conversation_flow = [software_development_readout_send]
        conversation_flow.append({"role": "user", "content": response})
        
        
        
        user_input = {"role": "user", "content": "How should we handle data visualization?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
                
        user_input = {"role": "user", "content": "What are features are missing in our project tree?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "What directories are currently missing files? What files should go under these directories?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        updated_project_tree = {"role": "user", "content": response}
        
        
        # We get final reset
        user_input = {"role": "user", "content": "Show me the complete project tree."}
        response = self.get_llm_response("Project Manager", conversation_flow)
        
        
        print('third checkpoint')
        self.raw_project_tree = response
        
        # Now We Reset context before we get too big
        conversation_flow = [software_development_readout_send]
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How do we handle our dependencies and requirements?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        
        user_input = {"role": "user", "content": "How should we handle deployment and containerization?"}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Add your recommendations to the project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})
        

        user_input = {"role": "user", "content": "Show me the complete project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        updated_project_tree = {"role": "user", "content": response}
        
        # We save this in case we want to talk to the project manager more before we proceed to development
        self.raw_project_tree = response
        
        
        # We convert the project tree in a manner that enables the Software Development team to iterate through files during development.
        user_input = {"role": "user", 
                      "content": '''convert this into a txt file that contains all files with their full paths included.
                      example: github-repository-name/.git
                      
                      Your responses should always follow this format:
                      github-repository-name/.git
                      github-repository-name/README.md
                      
                      '''}
        self.project_tree = self.get_llm_response("Project Manager", [software_development_readout_send, 
                                                  updated_project_tree, 
                                                  user_input])
        return self.project_tree


    def ask_project_manager_more(self, question):
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        
        # Now We Reset context before we get too big and add our last checkpoint
        conversation_flow = [software_development_readout_send]
        conversation_flow.append({"role": "assistant", "content": self.raw_project_tree })
        
        user_input = {"role": "user", "content": question}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        conversation_flow.append({"role": "user", "content": response})

        user_input = {"role": "user", "content": "Show me the complete project tree."}
        conversation_flow.append(user_input)
        response = self.get_llm_response("Project Manager", conversation_flow)
        updated_project_tree = {"role": "user", "content": response}
        
        # We save this in case we want to talk to the project manager more before we proceed to development
        self.raw_project_tree = response
        
        
        # We convert the project tree in a manner that enables the Software Development team to iterate through files during development.
        user_input = {"role": "user", 
                      "content": '''convert this into a txt file that contains all files with their full paths included.
                      example: github-repository-name/.git
                      
                      Your responses should always follow this format:
                      github-repository-name/.git
                      github-repository-name/README.md
                      
                      '''}
        self.project_tree = self.get_llm_response("Project Manager", [software_development_readout_send, 
                                                  updated_project_tree, 
                                                  user_input])
        return self.project_tree

    def simulate_development_conversation(self, start_point: Union[str, None] = None, iterations=5):
        # Split up Project Tree
        tmp_project_tree = self.project_tree.split('\n')
        for each in project_tree:
            try:
                if '.git' in each:
                    tmp_project_tree.remove(each)
                    
                if '.md' in each:
                    tmp_project_tree.remove(each)
            except:
                pass
                
        while '' in tmp_project_tree:
            tmp_project_tree.remove('')
            
        idx = 0
        if start_point:
            try:
                idx = tmp_project_tree.index(start_point)
            except:
                pass
        
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        project_tree_send = {"role": "user", "content": '<Solutions Architect> {self.project_tree}'} 
        
        for each in tmp_project_tree[idx:]:
            filename = each
            file_send = {"role": "user", "content": f"NEXT FILE: {filename}"}
        
            consulting_conversation_flow = [software_development_readout_send, project_tree_send, file_send]
            development_conversation_flow = [software_development_readout_send, project_tree_send]
            
            # Sprint One
            for i in range(iterations):  # You can adjust the number of iterations as needed
                # Get the Lead Software Developer's response
                try:
                    if i != iterations-1:
                        
                        consulting_response = manager.get_llm_response("Solutions Architect", consulting_conversation_flow)
                        consulting_send = {"role": "user", "content": consulting_response}
                        development_conversation_flow.append(consulting_send)
                        
                        # Get the Software Developer's response
                        dev_response = manager.get_llm_response("Software Developer", development_conversation_flow, filename=filename)
                        dev_send = {"role": "user", "content": dev_response}
                        consulting_conversation_flow.append(dev_send)
                    else:
                        final_line = {"role": "user", "content": "<Solution Architect> \nExcellent work. Show the complete code for {filename}"}
                        evelopment_conversation_flow.append(final_line)
                        
                        # Get the Software Developer's response
                        dev_response = manager.get_llm_response("Software Developer", development_conversation_flow, filename=filename)
                        dev_send = {"role": "user", "content": dev_response}
                        consulting_conversation_flow.append(dev_send)
                        
                        
                except Exception as e:
                    print(str(e)*10)
                    

    def update_file(self, filename, iterations=5):
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        project_tree_send = {"role": "user", "content": '<Solutions Architect> {self.project_tree}'} 
        
        file_send = {"role": "user", "content": f"NEXT FILE: {filename}"}
            
        file_content_send = {"role": "user", "content": f"<@Solutions Architect>{self.files[filename]}"}
    
        consulting_conversation_flow = [software_development_readout_send, project_tree_send, file_send, file_content_send]
        development_conversation_flow = [software_development_readout_send, project_tree_send]
        
        # Sprint One
        for i in range(iterations):  # You can adjust the number of iterations as needed
            # Get the Lead Software Developer's response
            try:
                consulting_response = manager.get_llm_response("Solutions Architect", consulting_conversation_flow)
                consulting_send = {"role": "user", "content": consulting_response}
                development_conversation_flow.append(consulting_send)
            
                # Get the Software Developer's response
                dev_response = manager.get_llm_response("Software Developer", development_conversation_flow, filename=filename)
                dev_send = {"role": "user", "content": dev_response}
                consulting_conversation_flow.append(dev_send)
            except Exception as e:
                print(str(e)*10)
                
    def replace_file(self, filename, iterations=5):
        software_development_readout_send = {"role": "user", "content": self.software_development_readout}
        project_tree_send = {"role": "user", "content": '<Solutions Architect> {self.project_tree}'} 
        
        file_send = {"role": "user", "content": f"NEXT FILE: {filename}"}
    
        consulting_conversation_flow = [software_development_readout_send, project_tree_send, file_send]
        development_conversation_flow = [software_development_readout_send, project_tree_send]
        
        # Sprint One
        for i in range(iterations):  # You can adjust the number of iterations as needed
            # Get the Lead Software Developer's response
            try:
                consulting_response = manager.get_llm_response("Solutions Architect", consulting_conversation_flow)
                consulting_send = {"role": "user", "content": consulting_response}
                development_conversation_flow.append(consulting_send)
            
                # Get the Software Developer's response
                dev_response = manager.get_llm_response("Software Developer", development_conversation_flow, filename=filename)
                dev_send = {"role": "user", "content": dev_response}
                consulting_conversation_flow.append(dev_send)
            except Exception as e:
                print(str(e)*10)
        

    def create_technical_documentation(self):
        self.readme = manager.get_llm_response("Technical Writer", [ json.dumps(self.files), 'File to Write: LICENSE'])
        self.readme = manager.get_llm_response("Technical Writer", [ json.dumps(self.files), 'File to Write: README'])
        self.conduct = manager.get_llm_response("Technical Writer", [ json.dumps(self.files), 'File to Write: CONTRIBUTING'])       
        

    def start_qa_code_reviewer(self):
        self.revised_files = json.loads(self.get_llm_response("QA Code Reviewer", [json.dumps(self.files)]))

    def create_github_repo(self, name):
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {"name": name}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()["html_url"]
        else:
            logging.error(f"Failed to create repository: {response.content}")
            raise Exception(f"Failed to create repository: {response.content}")

    def add_file_to_repo(self, repo_name, filename, code):
        url = f"https://api.github.com/repos/{repo_name}/contents/{filename}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "message": f"Add {filename}",
            "content": base64.b64encode(code.encode()).decode('utf-8')
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code not in [200, 201]:
            logging.error(f"Failed to add file to repository: {response.content}")
            raise Exception(f"Failed to add file to repository: {response.content}")


