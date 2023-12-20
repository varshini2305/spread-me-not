# chainlit run fact_inference.py
import os
import chainlit as cl
from langchain.llms import CTransformers, LlamaCpp
from langchain import PromptTemplate, LLMChain
# Local Model and Configuration
local_llm = "zephyr-7b-alpha.Q4_K_S.gguf"  # Path to the local Zephyr-7B model file

config = {
    "max_new_tokens": 1024,
    "repetition_penalty": 1.1,
    "temperature": 0.5,
    "top_k": 50,
    "top_p": 0.9,
    "stream": True,
    "threads": int(os.cpu_count() / 2)
}

 # Make sure the model path is correct for your system!
llm_init = LlamaCpp(
    model_path="zephyr-7b-alpha.Q4_K_S.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1
)

claim = "Israel lied about the 40 beheaded babies but they actually cut electricity to the hospital slowly suffocating Palestinian babies to death"
similar_result = """The narrator of the video says that “no evidence has been provided” for the viral claim that “40 babies” were “beheaded” by Hamas. That is true.

The Israeli government has posted graphic photos that purportedly show babies who were killed and/or burned by the militant group, but there were no photos showing decapitations. """


template = f"""
Check if the given text is confirming or denying the claim, or if there is no sufficient information provided to verify the claim. 
brief - explain briefly why the claim is valid (if there is supporting evidence), invalid (if there is no evidence, or there is opposite evidence), unverified(if no sufficient info)
verification_status - 'valid', 'invalid' or 'unverified'
return: [verification_status, brief]
Review text: '''claim: {claim}, text: {similar_result}'''
"""


@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=['question'])
    llm_chain = LLMChain(prompt=prompt, llm=llm_init, verbose=True)
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: str):
    llm_chain = cl.user_session.get("llm_chain")
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res["text"]).send()