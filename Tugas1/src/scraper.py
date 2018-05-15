import sys
import argparse
import time
import json
import requests
import lxml.html
from lxml.cssselect import CSSSelector as cs

yt_url = 'https://www.youtube.com/all_comments?v={yt_id}'
yt_ajax = 'https://www.youtube.com/comment_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

#Mendapatkan token
def find_value(html, key, num_chars=2):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find('"', pos_begin)
    return html[pos_begin: pos_end]

#Mendapatkan data-data dari suatu komentar
def extract_comments(html):
    tree = lxml.html.fromstring(html)
    item_sel = cs('.comment-item')
    text_sel = cs('.comment-text-content')
    time_sel = cs('.time')
    author_sel = cs('.user-name')

    for item in item_sel(tree):
        yield {'cid': item.get('data-cid'),
               'text': text_sel(item)[0].text_content(),
               'time': time_sel(item)[0].text_content().strip(),
               'author': author_sel(item)[0].text_content()}

#Mengambil data cid dari balasan komentar
def extract_reply_cids(html):
    tree = lxml.html.fromstring(html)
    sel = cs('.comment-replies-header > .load-comments')
    return [i.get('data-cid') for i in sel(tree)]


def ajax_request(session, url, params, data, retries=10, sleep=20):
    for _ in range(retries):
        response = session.post(url, params=params, data=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict.get('page_token', None), response_dict['html_content']
        else:
            time.sleep(sleep)

#Mengambil komentar dari video dengan id = yt_id
def download_comments(yt_id, sleep=1):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT

    # Laman youtube dengan komentar awal
    response = session.get(yt_url.format(yt_id=yt_id))
    html = response.text
    #mendapatkan cid dari komentar balasan
    reply_cids = extract_reply_cids(html)


    ret_cids = []
    for comment in extract_comments(html):
        ret_cids.append(comment['cid'])
        yield comment

    page_token = find_value(html, 'data-token')
    session_token = find_value(html, 'XSRF_TOKEN', 4)

    first_iteration = True

    #Mendapatkan komentar yang belum ditampilkan
    #Sama seperti menekan tombol "Show more"
    while page_token:
        data = {'video_id': yt_id,
                'session_token': session_token}

        params = {'action_load_comments': 1,
                  'order_by_time': True,
                  'filter': yt_id}

        if first_iteration:
            params['order_menu'] = True
        else:
            data['page_token'] = page_token

        response = ajax_request(session, yt_ajax, params, data)
        if not response:
            break

        page_token, html = response

        reply_cids += extract_reply_cids(html)
        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment

        first_iteration = False
        time.sleep(sleep)

    #Mendapatkan semua data komentar balasan (Get all replies)
    for cid in reply_cids:
        data = {'comment_id': cid,
                'video_id': yt_id,
                'can_reply': 1,
                'session_token': session_token}

        params = {'action_load_replies': 1,
                  'order_by_time': True,
                  'filter': yt_id,
                  'tab': 'inbox'}

        response = ajax_request(session, yt_ajax, params, data)
        if not response:
            break

        _, html = response

        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment
        time.sleep(sleep)

#Program utama
def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('\n\n--Youtube comment scraper--\n\n'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='If you happened to see this message, we all know you need some help, obviously')
    parser.add_argument('--youtubeid', '-y', help='ID of Youtube video that we need to scrape https://www.youtube.com/watch?v={youtubeid}')
    parser.add_argument('--outputfile', '-o', help='Output filename, end with .json')
    parser.add_argument('--limit', '-l', type=int, help='maximum number of comments you want to scrape, do not use it if you want to scrape all comments')

    try:
        args = parser.parse_args(argv)

        yt_id = args.youtubeid
        output = args.outputfile
        limit = args.limit

        #Error handler : argumen input kurang
        if not yt_id or not output:
            parser.print_usage()
            raise ValueError('Can you specify the youtubeid and the outputfile name, please?')

        print('\nNow we are ready to scrape Youtube comments for https://www.youtube.com/watch?v=', yt_id, '\n')
        count = 0
        with open(output, 'w') as fn:
            jsoncomment = []
            for comment in download_comments(yt_id):
                jsoncomment.append(comment)
                count += 1
                sys.stdout.write('%d comment(s) so far...\r' % count)
                if limit and count >= limit:
                    break
            json.dump(jsoncomment, fn)
            #Memasukkan data ke file output tanpa menunggu file diclose
            sys.stdout.flush()
        print('\nWe made it!')


    except Exception as e:
        print('Error:', str(e))
        sys.exit(1)

#Memanggil program utama
if __name__ == "__main__":
    main(sys.argv[1:])
