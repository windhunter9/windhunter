from lxml import html
import requests


def c():
  # Something
  return 2

def GetHtmlData(website):
	page = requests.get(website)
	tree = html.fromstring(page.content)
	return tree

def GetList(tree, xpath):
	return list(map(int, tree.xpath(xpath + '/text()')))


def GetText(tree, xpath):
	return tree.xpath(xpath +'/text()')
