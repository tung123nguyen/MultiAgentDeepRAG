"""Yaho Finance MC module with LangChain intergrate"""
import warnings 
warnings.filterwarnings("ignore")

import os
import sys

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

import asyncio 
from langchain_mcp_adapters.client import MultiServerMCPClient

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

system_prompt = """
You are a financial researcher agent helping users analyze stocks and financial data using Yahoo Finance.
Available Tools:
    - get_historical_stock_prices: Get historical stock prices (ticker required, optional: period='1mo', interval='1d')
    - get_stock_info: Get comprehensive stock information including: price, metrics, financials, etc.
     
"""