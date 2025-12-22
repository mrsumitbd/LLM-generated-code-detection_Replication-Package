import torch
import re

def preprocess(examples):
        new_examples = {"conversation": [], "input_ids": [], "loss_mask": []}

        for j in range(len(examples["messages"])):
            messages = []
            messages.extend(examples["messages"][j])
            conversation = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )

            if not tokenizer.pad_token_id:
                tokenizer.pad_token_id = tokenizer.unk_token_id

            input_ids = tokenizer(
                conversation,
                return_tensors="pt",
                add_special_tokens=False,
            ).input_ids[0]

            loss_mask = torch.zeros_like(input_ids)

            pattern = r"<\|im_start\|>assistant(.*?)<\|im_end\|>"

            responses = re.findall(pattern, conversation, re.DOTALL)

            for response in responses:
                search = tokenizer(
                    text=response,
                    return_tensors="pt",
                    add_special_tokens=False,
                ).input_ids[0]

                n = len(search)
                matches = [
                    i
                    for i in range(len(input_ids.tolist()) - n + 1)
                    if input_ids.tolist()[i : i + n] == search.tolist()
                ]
                loss_mask[matches[0] : matches[0] + n] = 1

            new_examples["conversation"].append(conversation)
            new_examples["input_ids"].append(input_ids[None, :])
            new_examples["loss_mask"].append(loss_mask[None, :])

        return new_examples