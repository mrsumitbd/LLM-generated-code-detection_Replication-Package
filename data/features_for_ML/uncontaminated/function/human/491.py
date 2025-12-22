from prompt import JUDGE_COT_PROMPT, JUDGE_PROMPT, MEMORY_COT_PROMPT, MEMORY_PROMPT, CONTEXT_COT_PROMPT, CONTEXT_PROMPT, CONTEXT_ENHANCE_EVAL_SYS, JUDGE_EVAL_SYS, MEMORY_EVAL_SYS, USR
from utils import OPENAI_API_KEY,OPENAI_BASE_URL,Global_Bio

def preprocess(sample, is_cot=False):
            if sample.get('assistant') is None and sample.get('enhanced_request') is not None:
                user_message = f"{USER_NAME}'s request is " + sample['user_request']
                infer_prompt = CONTEXT_COT_PROMPT.format(user_name=USER_NAME) if is_cot else CONTEXT_PROMPT.format(user_name=USER_NAME)
                messages = [
                    {"role": "system", "content": infer_prompt},
                    {"role": "user", "content": user_message},
                    # {"role": "assistant", "content": sample['enhanced_request'].strip('\n')},
                ]
                return [{"messages": messages,"user":user_message,"label":sample['enhanced_request'].strip('\n'),"eval_prompt":CONTEXT_ENHANCE_EVAL_SYS,"infer_prompt":infer_prompt}]
            if sample.get('assistant') is None and sample.get('user_feedback') is not None:
                user_message = f"{USER_NAME}'s request is " + sample['user_request'] + "\n" + "The response of expert is " + sample['expert_response']
                infer_prompt = JUDGE_COT_PROMPT.format(user_name=USER_NAME) if is_cot else JUDGE_PROMPT.format(user_name=USER_NAME)
                messages = [
                    {"role": "system", "content": infer_prompt},
                    {"role": "user", "content": user_message},
                    # {"role": "assistant", "content": sample['user_feedback'].strip('\n')},
                ]
                global_bio = Global_Bio
                return [{"messages": messages,"user":user_message,"label":sample['user_feedback'].strip('\n'),"eval_prompt":JUDGE_EVAL_SYS.format(global_bio=global_bio),"infer_prompt":infer_prompt}]
            sample['assistant'] = sample['assistant'].strip('\n')
            if sample.get('timestamp') is not None and sample.get('is_timeqa', None) is None:
                # messages1 = [
                #     {"role": "system", "content": "You are a helpful assistant.\n\nThe current date is " + sample['timestamp'][:10]},
                #     {"role": "user", "content": "<|ME|>" + sample['user']},
                #     {"role": "assistant", "content": sample['assistant']},
                # ]
                messages2 = [
                    {"role": "system", "content": ""},
                    {"role": "user", "content": "<|ME|>" + sample['user']},
                    {"role": "assistant", "content": sample['assistant']},
                ]
                if 'None' in sample['assistant']:
                    return []
                # return [{"content": tokenizer.apply_chat_template(messages1, tokenize=False)}, 
                #         {"content": tokenizer.apply_chat_template(messages2, tokenize=False)}]
                return [{"messages": messages2}]
            elif sample.get('is_timeqa', None) is not None:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant.\n\nToday’s date is " + sample['timestamp']},
                    {"role": "user", "content": "<|ME|>" + sample['user']},
                    {"role": "assistant", "content": sample['assistant']},
                ]
                if 'None' in sample['assistant']:
                    return []
                return {"messages": messages}
            elif sample.get('exact_day', None) is not None:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "<|ME|>" + sample['user']},
                    {"role": "assistant", "content": sample['assistant']},
                ]
                return [{"messages": messages}]
            else:
                infer_prompt = MEMORY_COT_PROMPT.format(user_name=USER_NAME) if is_cot else MEMORY_PROMPT.format(user_name=USER_NAME)
                messages = [
                    {"role": "system", "content": infer_prompt},
                    {"role": "user", "content": sample['user']},
                    # {"role": "assistant", "content": sample['assistant']},
                ]
                if 'None' in sample['assistant']:
                    return []
                return [{"messages": messages,"user":sample['user'],"label":sample['assistant'],"eval_prompt":MEMORY_EVAL_SYS,"infer_prompt":infer_prompt}]