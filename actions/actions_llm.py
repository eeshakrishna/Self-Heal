#actions_llm.py

import logging
import os
import random
from typing import Dict, Text, Any, List, Optional

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import re

DEFAULT_REPHRASE_RESPONSE = os.environ.get(
    "DEFAULT_REPHRASE_RESPONSE", "utter_ask_rephrase"
)

logger = logging.getLogger(__name__)

tokenizer = GPT2Tokenizer.from_pretrained('eeshakrishna2002/gpt2-TherapyV2')
model = GPT2LMHeadModel.from_pretrained('eeshakrishna2002/gpt2-TherapyV2')


def select_a_responses(
    domain: Dict[Text, Any], name: Text, channel: Text
) -> Optional[Text]:
    """
    Retrieves responses, filters by channel, and
    selects a random response among candidate responses
    """
    # retrieve responses
    responses = domain.get("responses", {}).get(name, [])

    # selecting the response at random
    # and based on the input channel
    responses = [
        response for response in responses if response.get("channel") in [None, channel]
    ]
    if not responses:
        return None

    response = random.choice(responses) if len(responses) > 1 else responses[0]
    return response.get("text", None)


class ActionLLMGenerateResponseTherapy(Action):
    """
    Trigger LLM API call to generate a specified response.
    To use this action, developers must ensure that there
    is a response with the utter_ prefix along with the name
    of the previous intent. This action then retrieves the
    response and generates a new response using a specified LLM.

    In addition, this action is capable of utilizing custom
    prompts based on the name of the intent, and fallback to
    the default prompt if a prompt is not specified in the
    llm_prompts.yml file.
    """

    def name(self) -> Text:
        return "action_llm_generate_response_therapy"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        latest_intent = tracker.get_intent_of_latest_message()
        latest_query = tracker.latest_message.get("text", None)
        input_channel = tracker.get_latest_input_channel()

        if not latest_query or not latest_intent:
            dispatcher.utter_message(template=DEFAULT_REPHRASE_RESPONSE)
            logger.info(f"Could not retrieve the latest intent or user query")
            return []

        # retrieve responses for the input channel
        response = select_a_responses(
            domain=domain, name=f"utter_{latest_intent}", channel=input_channel
        )
        if not response:
            dispatcher.utter_message(template=DEFAULT_REPHRASE_RESPONSE)
            logger.info(
                f"Could not retrieve the response for intent: utter_{latest_intent}"
            )
            return []

        try:
            inputs = tokenizer.encode(latest_query, return_tensors="pt")

            if len(inputs.shape) == 1:
                inputs = inputs.unsqueeze(0)

            attention_mask = torch.ones_like(inputs)

            outputs = model.generate(inputs, max_length=60, num_return_sequences=1, attention_mask=attention_mask)

            generated_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            trimmed_response = generated_response.replace(latest_query,"").strip()
            text=re.sub(r'^[,.\s]+', '', trimmed_response)
            last_punct_index = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
            if last_punct_index != -1:
                text = text[:last_punct_index + 1]
            dispatcher.utter_message(text=text)
            logger.info(f"GPT-2 response generated")
        except Exception as e:
            dispatcher.utter_message(template=DEFAULT_REPHRASE_RESPONSE)
            logger.exception(
                f"An exception occurred while generating the GPT-2 response. "
                f"Falling back to the rephrase utterance. {e}"
            )

        return []
