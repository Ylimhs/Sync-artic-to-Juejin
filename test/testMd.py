import markdown
import re
import requests

def get_image_url(image_url):
    """从给定的图片链接获取新的链接"""
    return "https://example.com/replace1"
    response = requests.get('https://example.com/replace', params={'url': image_url})
    if response.status_code == 200:
        return response.json().get('new_url')
    else:
        return None

def html_replace_image_links(html_text):
    """解析Markdown文本中的图片链接并替换为动态获取的链接"""
    html_text = markdown.markdown(md_text)
    pattern = r'<img.*?src="(.*?)".*?>'
    replaced_html_text = html_text
    for match in re.findall(pattern, html_text):
        new_url = get_image_url(match)
        if new_url is not None:
            replaced_html_text = replaced_html_text.replace(match, new_url)
    return replaced_html_text


if __name__ == '__main__':
    md_text = 'This is a sample Markdown text with an ![example image](https://example.com/image.png).'
    ht_text = '<p>This is a sample Markdown text with an <img alt="example image" src="https://example.com/replace" />.</p>'
    replaced_text = html_replace_image_links(ht_text)
    print(replaced_text)

    print(20 < 20)