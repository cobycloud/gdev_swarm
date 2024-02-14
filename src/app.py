from barfi import st_barfi, barfi_schemas, Block
import streamlit as st
from barfi import Block
from ContextManager import *


#####################################################################

manager = ContextManager("your-github-token", 
                         "./ContextManager/context/V2/PromptEngineer.txt", 
                         "./ContextManager/context/V2/PromptEngineerV2.txt", 
                         "./ContextManager/context/V2/PromptEngineerV3.txt", 
                         "./ContextManager/context/V2/SolutionsArchitect.txt", 
                         "./ContextManager/context/V2/SoftwareDeveloper.txt", 
                         "./ContextManager/context/V2/GithubAdmin.txt", 
                         "./ContextManager/context/V2/TechnicalWriter.txt", 
                         "./ContextManager/context/V2/QACodeReviewer.txt", 
                         "./ContextManager/context/V2/ProjectManager.txt",
                         )

user_input = Block(name='Product User Input')
user_input.add_output(name='Product User Input')
def user_input_func(self):

    value = globals()['prompt']
    print(f"Product User Input: {value}")
    self.set_interface(name="Product User Input", value=value)
    
user_input.add_compute(user_input_func)


#####################################################################

create_role = Block(name='Create Role Context')
create_role.add_input(name='Product User Input')
create_role.add_input(name='Role Name')
create_role.add_output(name='Role')
create_role.add_output(name='Context')

def f_create_role(self):
    in_1 = self.get_interface(name="Product User Input")
    in_2 = self.get_interface(name="Role Name")
    
    context =manager.generate_role_contexts(in_1, in_2)

    self.set_interface(name='Role', value=in_2)
    self.set_interface(name='Context', value=context)
    
create_role.add_compute(f_create_role)

#####################################################################


create_role_v2_data = Block(name='Context Data')
create_role_v2_data.add_option(name='Role Name Input', type="input", value="")
create_role_v2_data.add_option(name='Goal Input', type="input", value="")
create_role_v2_data.add_option(name='Nongoal Input', type="input", value="")
create_role_v2_data.add_option(name='Listen To Input', type="input", value="")
create_role_v2_data.add_option(name='Respond To Input', type="input", value="")
create_role_v2_data.add_option(name='Work Input', type="input", value="")
create_role_v2_data.add_option(name='Key Name of Work Input', type="input", value="")
create_role_v2_data.add_option(name='Request Input', type="input", value="")
create_role_v2_data.add_option(name='Key Name of Request Input', type="input", value="")

create_role_v2_data.add_output(name='Role Name Output')
create_role_v2_data.add_output(name='Goal Output')
create_role_v2_data.add_output(name='Nongoal Output')
create_role_v2_data.add_output(name='Listen To Output')
create_role_v2_data.add_output(name='Respond To Output')
create_role_v2_data.add_output(name='Work Output')
create_role_v2_data.add_output(name='Key Name of Work Output')
create_role_v2_data.add_output(name='Request Output')
create_role_v2_data.add_output(name='Key Name of Request Output')


def f_create_role_v2_data(self):
    try:
        opt_2 = self.get_option(name="Role Name Input")
        opt_3 = self.get_option(name="Goal Input")
        opt_4 = self.get_option(name="Nongoal Input")
        opt_5 = self.get_option(name="Listen To Input")
        opt_6 = self.get_option(name="Respond To Input")
        opt_7 = self.get_option(name="Work Input")
        opt_8 = self.get_option(name="Key Name of Work Input")
        opt_9 = self.get_option(name="Request Input")
        opt_10 = self.get_option(name="Key Name of Request Input")


        self.set_interface(name="Role Name Output", value=opt_2)
        self.set_interface(name="Goal Output", value=opt_3)
        self.set_interface(name="Nongoal Output", value=opt_4)
        self.set_interface(name="Listen To Output", value=opt_5)
        self.set_interface(name="Respond To Output", value=opt_6)
        self.set_interface(name="Work Output", value=opt_7)
        self.set_interface(name="Key Name of Work Output", value=opt_8)
        self.set_interface(name="Request Output", value=opt_9)
        self.set_interface(name="Key Name of Request Output", value=opt_10)
        
        
    except Exception as e:
        print(f"f_create_role_v2_data error: {e}")
    
    
create_role_v2_data.add_compute(f_create_role_v2_data)

#####################################################################

create_role_v2 = Block(name='Create Role Context V2')
create_role_v2.add_input(name='Product User Input')
create_role_v2.add_input(name='Role Name')
create_role_v2.add_input(name='Goal')
create_role_v2.add_input(name='Nongoal')
create_role_v2.add_input(name='Listen To')
create_role_v2.add_input(name='Respond To')
create_role_v2.add_input(name='Output')
create_role_v2.add_input(name='Key Name of Output')
create_role_v2.add_input(name='Request')
create_role_v2.add_output(name='Output Key Name')
create_role_v2.add_output(name='Role')
create_role_v2.add_output(name='Context')

def f_create_role_v2(self):
    try:
        in_1 = self.get_interface(name="Product User Input")
        in_2 = self.get_interface(name="Role Name")
        in_3 = self.get_interface(name="Goal")
        in_4 = self.get_interface(name="Nongoal")
        in_5 = self.get_interface(name="Listen To")
        in_6 = self.get_interface(name="Respond To")
        in_7 = self.get_interface(name="Output")
        in_8 = self.get_interface(name="Key Name of Output")
        in_9 = self.get_interface(name="Request")


        if in_5 == None:
            in_5 = ''

        if in_6 == None:
            in_6 = ''

        if in_9 == None:
            in_9 = ''


        context = manager.generate_role_context_v2(product=in_1, 
            role=in_2, 
            goal=in_3, 
            nongoal=in_4, 
            listen_to=in_5, 
            respond_to=in_6, 
            output=in_7,
            request=in_9)
        self.set_interface(name="Output Key Name", value=in_8)
        self.set_interface(name="Role", value=in_2)
        self.set_interface(name="Context", value=context)
        
        
    except Exception as e:
        print(f"f_create_role_v2 error: {e}")
    
    
create_role_v2.add_compute(f_create_role_v2)

#####################################################################
role_context_response = Block(name="Role Context Response")
role_context_response.add_input(name="Role")
role_context_response.add_input(name="Context")
role_context_response.add_input(name="Conversation Array")
role_context_response.add_output(name="Response Output")
role_context_response.add_output(name="Role Output")
role_context_response.add_output(name="Context Output")
def role_context_response_func(self):
    in_1 = self.get_interface(name="Role")
    in_2 = self.get_interface(name="Context")
    in_3 = self.get_interface(name="Conversation Array")


    

    if in_3 == None or in_3 == []:
        out_1 = manager.get_llm_response_from_context(in_2, conversation_flow=None, role=in_1)
    else:
        out_1 = manager.get_llm_response_from_context(in_2, conversation_flow=in_3, role=in_1)


    self.set_interface(name="Response Output", value=out_1)
    self.set_interface(name="Role Output", value=in_1)
    self.set_interface(name="Context Output", value=in_2)
    
role_context_response.add_compute(role_context_response_func)

#####################################################################
multi_context_response = Block(name="Multi-Context Response")
multi_context_response.add_input(name="Append Conversation")

multi_context_response.add_input(name="Role Input 1")
multi_context_response.add_input(name="Context Input 1")
multi_context_response.add_input(name="Conversation Input 1")

multi_context_response.add_input(name="Role Input 2")
multi_context_response.add_input(name="Context Input 2")
multi_context_response.add_input(name="Conversation Input 2")

multi_context_response.add_input(name="Role Input 3")
multi_context_response.add_input(name="Context Input 3")
multi_context_response.add_input(name="Conversation Input 3")

multi_context_response.add_input(name="Role Input 4")
multi_context_response.add_input(name="Context Input 4")
multi_context_response.add_input(name="Conversation Input 4")

multi_context_response.add_output(name="Response Output 1")
multi_context_response.add_output(name="Role Output 1")
multi_context_response.add_output(name="Context Output 1")

multi_context_response.add_output(name="Response Output 2")
multi_context_response.add_output(name="Role Output 2")
multi_context_response.add_output(name="Context Output 2")

multi_context_response.add_output(name="Response Output 3")
multi_context_response.add_output(name="Role Output 3")
multi_context_response.add_output(name="Context Output 3")

multi_context_response.add_output(name="Response Output 4")
multi_context_response.add_output(name="Role Output 4")
multi_context_response.add_output(name="Context Output 4")


def f_multi_context_response(self):
    try:
        append_conversation = self.get_interface(name="Append Conversation")

        role_in_1 = self.get_interface(name="Role Input 1")
        context_in_1 = self.get_interface(name="Context Input 1")
        conversation_in_1 = self.get_interface(name="Conversation Input 1")

        if role_in_1 and context_in_1:
            if conversation_in_1 == None or conversation_in_1 == []:

                if append_conversation:
                    print('now', conversation_in_1)
                    out_1 = manager.get_llm_response_from_context(context_in_1, conversation_flow=append_conversation, role=role_in_1)
                else:
                    print('there', conversation_in_1)
                    out_1 = manager.get_llm_response_from_context(context_in_1, conversation_flow=None, role=role_in_1)
            else:
                conversation_in_1.extend(append_conversation)
                print('here', conversation_in_1)
                out_1 = manager.get_llm_response_from_context(context_in_1, conversation_flow=conversation_in_1, role=role_in_1)


            self.set_interface(name="Response Output 1", value=out_1)
            self.set_interface(name="Role Output 1", value=role_in_1)
            self.set_interface(name="Context Output 1", value=context_in_1)

        role_in_2 = self.get_interface(name="Role Input 2")
        context_in_2 = self.get_interface(name="Context Input 2")
        conversation_in_2 = self.get_interface(name="Conversation Input 2")

        if role_in_2 and context_in_2:

            if conversation_in_2 == None or conversation_in_2 == []:
                if append_conversation:
                    out_2 = manager.get_llm_response_from_context(context_in_2, conversation_flow=append_conversation, role=role_in_2)
                else:
                    out_2 = manager.get_llm_response_from_context(context_in_2, conversation_flow=None, role=role_in_2)
            else:
                conversation_in_2.extend(append_conversation)
                out_2 = manager.get_llm_response_from_context(context_in_2, conversation_flow=conversation_in_2, role=role_in_2)


            self.set_interface(name="Response Output 2", value=out_2)
            self.set_interface(name="Role Output 2", value=role_in_2)
            self.set_interface(name="Context Output 2", value=context_in_2)

        role_in_3 = self.get_interface(name="Role Input 3")
        context_in_3 = self.get_interface(name="Context Input 3")
        conversation_in_3 = self.get_interface(name="Conversation Input 3")

        if role_in_3 and context_in_3:

            if conversation_in_3 == None or conversation_in_3 == []:
                if append_conversation:
                    out_3 = manager.get_llm_response_from_context(context_in_3, conversation_flow=append_conversation, role=role_in_3)
                else:
                    out_3 = manager.get_llm_response_from_context(context_in_3, conversation_flow=None, role=role_in_3)
            else:
                conversation_in_3.extend(append_conversation)
                out_3 = manager.get_llm_response_from_context(context_in_3, conversation_flow=conversation_in_3, role=role_in_3)


            self.set_interface(name="Response Output 3", value=out_3)
            self.set_interface(name="Role Output 3", value=role_in_3)
            self.set_interface(name="Context Output 3", value=context_in_3)


        role_in_4 = self.get_interface(name="Role Input 4")
        context_in_4 = self.get_interface(name="Context Input 4")
        conversation_in_4 = self.get_interface(name="Conversation Input 4")
        if role_in_4 and context_in_4:

            if conversation_in_4 == None or conversation_in_4 == []:
                if append_conversation:
                    out_4 = manager.get_llm_response_from_context(context_in_4, conversation_flow=append_conversation, role=role_in_4)
                else:
                    out_4 = manager.get_llm_response_from_context(context_in_4, conversation_flow=None, role=role_in_4)
            else:
                conversation_in_4.extend(append_conversation)
                out_4 = manager.get_llm_response_from_context(context_in_4, conversation_flow=conversation_in_4, role=role_in_4)


            self.set_interface(name="Response Output 4", value=out_4)
            self.set_interface(name="Role Output 4", value=role_in_4)
            self.set_interface(name="Context Output 4", value=context_in_4)
    except Exception as e:
        print(f"f_multi_context_response error: {e}")
    
multi_context_response.add_compute(f_multi_context_response)



################################################################################







create_role_v3_data = Block(name='Context Data')
create_role_v3_data.add_option(name='Role Name Input', type="input", value="")
create_role_v3_data.add_option(name='Goal Input', type="input", value="")
create_role_v3_data.add_option(name='Nongoal Input', type="input", value="")
create_role_v3_data.add_option(name='Listen To Input', type="input", value="")
create_role_v3_data.add_option(name='Respond To Input', type="input", value="")
create_role_v3_data.add_option(name='Work Input', type="input", value="")
create_role_v3_data.add_option(name='Key Name of Work Input', type="input", value="")
create_role_v3_data.add_option(name='Request Input', type="input", value="")
create_role_v3_data.add_option(name='Key Name of Request Input', type="input", value="")

create_role_v3_data.add_output(name='Role Name Output')
create_role_v3_data.add_output(name='Goal Output')
create_role_v3_data.add_output(name='Nongoal Output')
create_role_v3_data.add_output(name='Listen To Output')
create_role_v3_data.add_output(name='Respond To Output')
create_role_v3_data.add_output(name='Work Output')
create_role_v3_data.add_output(name='Key Name of Work Output')
create_role_v3_data.add_output(name='Request Output')
create_role_v3_data.add_output(name='Key Name of Request Output')


def f_create_role_v3_data(self):
    try:
        opt_2 = self.get_option(name="Role Name Input")
        opt_3 = self.get_option(name="Goal Input")
        opt_4 = self.get_option(name="Nongoal Input")
        opt_5 = self.get_option(name="Listen To Input")
        opt_6 = self.get_option(name="Respond To Input")
        opt_7 = self.get_option(name="Work Input")
        opt_8 = self.get_option(name="Key Name of Work Input")
        opt_9 = self.get_option(name="Request Input")
        opt_10 = self.get_option(name="Key Name of Request Input")


        self.set_interface(name="Role Name Output", value=opt_2)
        self.set_interface(name="Goal Output", value=opt_3)
        self.set_interface(name="Nongoal Output", value=opt_4)
        self.set_interface(name="Listen To Output", value=opt_5)
        self.set_interface(name="Respond To Output", value=opt_6)
        self.set_interface(name="Work Output", value=opt_7)
        self.set_interface(name="Key Name of Work Output", value=opt_8)
        self.set_interface(name="Request Output", value=opt_9)
        self.set_interface(name="Key Name of Request Output", value=opt_10)
        
        
    except Exception as e:
        print(f"f_create_role_v3_data error: {e}")
    
    
create_role_v3_data.add_compute(f_create_role_v3_data)

#####################################################################

create_role_v3 = Block(name='Create Role Context V3')
create_role_v3.add_input(name='Product User Input')
create_role_v3.add_input(name='Role Name')
create_role_v3.add_input(name='Goal')
create_role_v3.add_input(name='Nongoal')
create_role_v3.add_input(name='Listen To')
create_role_v3.add_input(name='Respond To')
create_role_v3.add_input(name='Output')
create_role_v3.add_input(name='Key Name of Output')
create_role_v3.add_input(name='Request')
create_role_v3.add_output(name='Output Key Name')
create_role_v3.add_output(name='Role')
create_role_v3.add_output(name='Context')

def f_create_role_v3(self):
    try:
        in_1 = self.get_interface(name="Product User Input")
        in_2 = self.get_interface(name="Role Name")
        in_3 = self.get_interface(name="Goal")
        in_4 = self.get_interface(name="Nongoal")
        in_5 = self.get_interface(name="Listen To")
        in_6 = self.get_interface(name="Respond To")
        in_7 = self.get_interface(name="Output")
        in_8 = self.get_interface(name="Key Name of Output")
        in_9 = self.get_interface(name="Request")


        if in_5 == None:
            in_5 = ''

        if in_6 == None:
            in_6 = ''

        if in_9 == None:
            in_9 = ''


        context = manager.generate_role_context_v3(product=in_1, 
            role=in_2, 
            goal=in_3, 
            nongoal=in_4, 
            listen_to=in_5, 
            respond_to=in_6, 
            output=in_7,
            need=in_9)
        self.set_interface(name="Output Key Name", value=in_8)
        self.set_interface(name="Role", value=in_2)
        self.set_interface(name="Context", value=context)
        
        
    except Exception as e:
        print(f"f_create_role_v3 error: {e}")
    
    
create_role_v3.add_compute(f_create_role_v3)

#####################################################################

create_role_from_var_arr = Block(name='Create Context from Var')
create_role_from_var_arr.add_input(name='Role Name')
create_role_from_var_arr.add_input(name='Variable Array')
create_role_from_var_arr.add_output(name='Role')
create_role_from_var_arr.add_output(name='Context')
def f_create_role_from_var_arr(self):
    try:
        in_1 = self.get_interface(name="Role Name")
        in_2 = self.get_interface(name="Variable Array")

        if type(in_2) != list:
            in_2 = [in_2]


        context = manager.generate_role_context_v4(role=in_1, variables=in_2)
        self.set_interface(name="Role", value=in_1)
        self.set_interface(name="Context", value=context)
        
    except Exception as e:
        print(f"f_create_role_from_var_arr error: {e}")
    
    
create_role_from_var_arr.add_compute(f_create_role_from_var_arr)

#####################################################################




append_user_msg = Block(name="Append User Msg")
append_user_msg.add_input(name="Unwrapped Response")
append_user_msg.add_input(name="Conversation Flow")
append_user_msg.add_output(name="Updated Conversation Flow")
def f_append_user_msg(self):
    in_1 = self.get_interface(name="Unwrapped Response")
    in_2 = self.get_interface(name="Conversation Flow")

    if in_2:
        in_2.append({"role": "user", "content": in_1})
    else:
        in_2 = [{"role": "user", "content": in_1}]

    value = in_2
    self.set_interface(name="Updated Conversation Flow", value=value)
    
append_user_msg.add_compute(f_append_user_msg)

#####################################################################
append_asst_msg = Block(name="Append Asst Msg")
append_asst_msg.add_input(name="Unwrapped Response")
append_asst_msg.add_input(name="Conversation Flow")
append_asst_msg.add_output(name="Updated Conversation Flow")
def f_append_asst_msg(self):
    in_1 = self.get_interface(name="Unwrapped Response")
    in_2 = self.get_interface(name="Conversation Flow")

    if in_2:
        in_2.append({"role": "assistant", "content": in_1})
    else:
        in_2 = [{"role": "assistant", "content": in_1}]

    value = in_2
    self.set_interface(name="Updated Conversation Flow", value=value)
    
append_asst_msg.add_compute(f_append_asst_msg)



#####################################################################
context_response = Block(name="Context Response")
context_response.add_input(name="Context")
context_response.add_input(name="Conversation Array")
context_response.add_output(name="Response")
def context_response_func(self):
    in_1 = self.get_interface(name="Context")
    in_2 = self.get_interface(name="Conversation Array")
    


    if in_2 == []:
        out_1 = manager.get_llm_response_from_context(in_1, None)
    else:
        out_1 = manager.get_llm_response_from_context(in_1, in_2)


    self.set_interface(name="Response", value=out_1)
    
context_response.add_compute(context_response_func)


#####################################################################


empty_array = Block(name="Empty Array")
empty_array.add_output(name="Empty Array")
def empty_array_func(self):
    self.set_interface(name="Empty Array", value=[])
    
empty_array.add_compute(empty_array_func)


#####################################################################

append_message = Block(name="Append Message to Conversation Flow")
append_message.add_input(name="Message")
append_message.add_input(name="Conversation Array")
append_message.add_output(name="Updated Conversation Array")
def append_message_func(self):
    in_1 = self.get_interface(name="Message")
    in_2 = self.get_interface(name="Conversation Array")

    in_2.append(in_1)
    out_1 = in_2

    self.set_interface(name="Updated Conversation Array", value=out_1)
    
append_message.add_compute(append_message_func)


#####################################################################

wrap_response_into_user_msg = Block(name="Wrapped User Message")
wrap_response_into_user_msg.add_input(name="Unwrapped Response")
wrap_response_into_user_msg.add_output(name="Wrapped Response")
def wrap_response_into_user_msg_func(self):
    in_1 = self.get_interface(name="Unwrapped Response")
    out_1 = {"role": "user", "content": in_1}
    self.set_interface(name="Wrapped Response", value=out_1)
    
wrap_response_into_user_msg.add_compute(wrap_response_into_user_msg_func)

#####################################################################
wrap_response_into_assistant_msg = Block(name="Wrapped Assistant Message")
wrap_response_into_assistant_msg.add_input(name="Unwrapped Response")
wrap_response_into_assistant_msg.add_output(name="Wrapped Response")
def wrap_response_into_assistant_msg_func(self):
    in_1 = self.get_interface(name="Unwrapped Response")
    out_1 = {"role": "assistant", "content": in_1}
    self.set_interface(name="Wrapped Response", value=out_1)
    
wrap_response_into_assistant_msg.add_compute(wrap_response_into_assistant_msg_func)

#####################################################################
save_result_as = Block(name="Save Result As")
save_result_as.add_input(name="Key Name")
save_result_as.add_input(name="Unwrapped Response")
save_result_as.add_output(name="Key Name Output")
def save_result_as_func(self):
    try:
        in_1 = self.get_interface(name="Key Name")
        in_2 = self.get_interface(name="Unwrapped Response")
        self.set_interface(name="Key Name Output", value=in_1)
        manager[in_1] = in_2
    except Exception as e:
        print(f"save_result_as_func error: {e}")

    
save_result_as.add_compute(save_result_as_func)

#####################################################################
get_result_of = Block(name="Get Result Of")
get_result_of.add_input(name="Key Name")
get_result_of.add_output(name="Unwrapped Response")
def get_result_of_func(self):
    try:
        in_1 = self.get_interface(name="Key Name")
        result = manager[in_1]
        in_2 = self.set_interface(name="Unwrapped Response", value=result)
    except Exception as e:
        print(f"get_result_of_func error: {e}")
    
    
get_result_of.add_compute(get_result_of_func)

#####################################################################

splitter = Block(name='Splitter')
splitter.add_input()
splitter.add_output()
splitter.add_output()
def splitter_func(self):
    in_1 = self.get_interface(name='Input 1')
    self.set_interface(name='Output 1', value=in_1)
    self.set_interface(name='Output 2', value=in_2)
    
splitter.add_compute(splitter_func)


#####################################################################

string_block = Block(name='String')
string_block.add_option(name="Prompt Value", type="input")
string_block.add_output(name="String")
def string_block_func(self):
    opt_1 = self.get_option(name="Prompt Value")    
    self.set_interface(name="String", value=opt_1)
string_block.add_compute(string_block_func)

#####################################################################

select_block = Block(name='Select')
select_block.add_option(name="Prompt Value", type="select", items=["1","2","3"])
def f_select_block(self):
    opt_1 = self.get_option(name="Prompt Value") 
select_block.add_compute(f_select_block)

#####################################################################

keypair = Block(name='Key Pair')
keypair.add_option(name="Key Name Option 1", type="input", value="")
keypair.add_option(name="Key Value Option 2", type="input", value="")
keypair.add_output(name="Keypair Output 1")
def f_keypair(self):
    in_1 = self.get_option(name="Key Name Option 1")
    in_2 = self.get_option(name="Key Value Option 2")
    self.set_interface(name="Keypair Output 1", value={in_1:in_2})
            
keypair.add_compute(f_keypair)

#####################################################################

add_keypair = Block(name="Key Pair Array")
add_keypair.add_input(name="Keypair Input 1")
add_keypair.add_input(name="Keypair Array Input 2")
add_keypair.add_output(name="Updated Keypair Output 1")
def f_add_keypair(self):
    in_1 = self.get_interface(name="Keypair Input 1")
    in_2 = self.get_interface(name="Keypair Array Input 2")
    in_2.append(in_1)

    value = in_2
    self.set_interface(name="Updated Keypair Output 1", value=value)
            
add_keypair.add_compute(f_add_keypair)

#####################################################################

four_in_one_keypair = Block(name="4:1 Key Pair Array")
four_in_one_keypair.add_input(name="Keypair Input 1")
four_in_one_keypair.add_input(name="Keypair Input 2")
four_in_one_keypair.add_input(name="Keypair Input 3")
four_in_one_keypair.add_input(name="Keypair Input 4")
four_in_one_keypair.add_output(name="Updated Keypair Output 1")
def f_four_in_one_keypair(self):
    in_1 = self.get_interface(name="Keypair Input 1")
    in_2 = self.get_interface(name="Keypair Input 2")
    in_3 = self.get_interface(name="Keypair Input 3")
    in_4 = self.get_interface(name="Keypair Input 4")
    
    value = []

    if in_1:
        value.append(in_1)

    if in_2:
        value.append(in_2)

    if in_3:
        value.append(in_3)

    if in_4:
        value.append(in_4)

    self.set_interface(name="Updated Keypair Output 1", value=value)
            
four_in_one_keypair.add_compute(f_four_in_one_keypair)

#####################################################################

concat_string = Block(name="Concat String")
concat_string.add_input(name="String Input 1")
concat_string.add_input(name="String Input 2")
concat_string.add_output(name="Updated String Output 1")
def f_concat_string(self):
    in_1 = self.get_interface(name="String Input 1")
    in_2 = self.get_interface(name="String Input 2")


    value = in_1 + in_2
    
    self.set_interface(name="Updated String Output 1", value=value)
            
concat_string.add_compute(f_concat_string)

#####################################################################

concat_array = Block(name="Concat Array")
concat_array.add_input(name="Array Input 1")
concat_array.add_input(name="Array Input 2")
concat_array.add_output(name="Updated Array Output 1")
def f_concat_array(self):
    in_1 = self.get_interface(name="Array Input 1")
    in_2 = self.get_interface(name="Array Input 2")


    value = []
    value.extend(in_1)
    value.extend(in_2)
    
    self.set_interface(name="Updated Array Output 1", value=value)
            
concat_array.add_compute(f_concat_array)

#####################################################################

or_block = Block(name="Or")
or_block.add_input(name="Input 1")
or_block.add_input(name="Input 2")
or_block.add_output(name="Output 1")
def f_or_block(self):
    in_1 = self.get_interface(name="Input 1")
    in_2 = self.get_interface(name="Input 2")


    value = in_1 or in_2
    
    self.set_interface(name="Output 1", value=value)
            
or_block.add_compute(f_or_block)

#####################################################################

printer = Block(name='Printer')
printer.add_input(name="Input 1")
printer.add_option(name="Title", type="input", value="")
def string_block_func(self):
    in_1 = self.get_interface(name="Input 1")
    opt_1 = self.get_option(name="Title")
    print(f"\n---\n{opt_1 or self._name}:\n {in_1}")
printer.add_compute(string_block_func)



#####################################################################

writer = Block(name='Writer')
writer.add_input(name="Input 1")
writer.add_option(name="Title", type="input", value="")
def f_writer(self):
    in_1 = self.get_interface(name="Input 1")
    opt_1 = self.get_option(name="Title")
    st.text(f"\n---\n{opt_1 or self._name}:\n {in_1}")
writer.add_compute(f_writer)

#####################################################################
st.set_page_config(
    page_title="swarm.az69",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://swarm.az69.xyz/help',
        'Report a bug': "https://swarm.az69.xyz/bug",
        'About': "#Swarm"
    }
)



project_name = st.text_input('project name?')
print(project_name)

prompt = st.text_area('prompt?', height=200)
print(prompt)
load_schema = st.selectbox('Select a saved schema:', barfi_schemas())

compute_engine = st.checkbox('Activate compute engine', value=False)

user_input_blocks = {"User Inputs": [user_input]}
utility_blocks = {"Utility": [string_block, concat_string, empty_array, keypair, concat_array, add_keypair, four_in_one_keypair]}
output_blocks = {"Outputs": [writer, printer]}
llm_blocks = {"Manager": [create_role, create_role_v2, create_role_v2_data, role_context_response, append_message, wrap_response_into_user_msg, wrap_response_into_assistant_msg]}

v3_llm_blocks = {"V3 Manager": [create_role_v3, create_role_v3_data, create_role_from_var_arr, multi_context_response, append_user_msg, append_asst_msg]}
memory_blocks = {"Memory": [save_result_as, get_result_of]}
logic_blocks = {"Logic": [or_block]}

base_blocks = {}
base_blocks.update(v3_llm_blocks)
base_blocks.update(utility_blocks)
base_blocks.update(output_blocks)
base_blocks.update(llm_blocks)
base_blocks.update(memory_blocks)
base_blocks.update(user_input_blocks)
base_blocks.update(logic_blocks)



barfi_result = st_barfi(base_blocks=base_blocks,
    compute_engine=compute_engine, load_schema=load_schema)



st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)



#if barfi_result:
    #st.write(barfi_result)

if manager.responses:
    st.write(manager.responses)
