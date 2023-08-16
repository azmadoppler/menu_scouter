
url = "https://j-doradic.com/eng-jp?q=a&searchPosition=searchBetween&page="
data = [] 
count = 0
for i in range(1,14123):
    print(i)
    new_link = url+str(i)
    result = requests.get(new_link)
    doc = BeautifulSoup(result.text,"html.parser")
    tbody = doc.tbody
    trs = tbody.contents
        
    for tr in trs:
        try:
            inner_content = tr.contents[1]
            kanji = inner_content.a.next
            temp = inner_content.find_all(['h3'])
            word = temp[0].next.next
            meaning = temp[1].next.next
            data.append([kanji,word,meaning])
        except:
            continue
    #print(tr)
    count= count+1

