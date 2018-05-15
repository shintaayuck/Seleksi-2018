<h1 align="center">
  <br>
  Tugas 1 Seleksi Warga Basdat 2018
  <br>
  <br>
</h1>

<h2 align="center">
  <br>
  Data Scraping : Youtube Comments Scraper
  <br>
  <br>
</h2>

A youtube comments https://www.youtube.com/all_comments?v={yt_id} scraper, made with Python3. yt_id is the youtube video ID which will be scraped. It collects comment ID, comment's content, comment's published time relative to scrape time, and author of the comment.

### Specifications

1. Lakukan data scraping dari sebuah laman web untuk memeroleh data atau informasi tertentu __TANPA MENGGUNAKAN API__

2. Daftarkan judul topik yang akan dijadikan bahan data scraping pada spreadsheet berikut: [Topik Data Scraping](http://bit.ly/TopikDataScraping). Usahakan agar tidak ada peserta dengan topik yang sama. Akses edit ke spreadsheet akan ditutup tanggal 10 Mei 2018 pukul 20.00 WIB

3. Dalam mengerjakan tugas 1, calon warga basdat terlebih dahulu melakukan fork project github pada link berikut: https://github.com/wargabasdat/Seleksi-2018/Tugas1. Sebelum batas waktu pengumpulan berakhir, calon warga basdat harus sudah melakukan pull request dengan nama ```TUGAS_SELEKSI_1_[NIM]```

4. Pada repository tersebut, calon warga basdat harus mengumpulkan file script dan json hasil data scraping. Repository terdiri dari folder src dan data dimana folder src berisi file script/kode yang __WELL DOCUMENTED dan CLEAN CODE__ sedangkan folder data berisi file json hasil scraper.

5. Peserta juga diminta untuk membuat Makefile sesuai template yang disediakan, sehingga program dengan gampang di-_build_, di-_run_, dan di-_clean_

``` Makefile
all: clean build run

clean: # remove data and binary folder

build: # compile to binary (if you use interpreter, then do not implement it)

run: # run your binary

```

6. Deadline pengumpulan tugas adalah __15 Mei 2018 Pukul 23.59__

7. Tugas 1 akan didemokan oleh masing-masing calon warga basdat

8. Demo tugas mencakup keseluruhan proses data scraping hingga memeroleh data sesuai dengan yang dikumpulkan pada Tugas 1

9. Hasil data scraping ini nantinya akan digunakan sebagai bahan tugas analisis dan visualisasi data

10. Sebagai referensi untuk mengenal data scraping, asisten menyediakan dokumen "Short Guidance To Data Scraping" yang dapat diakses pada link berikut: [Data Scraping Guidance](bit.ly/DataScrapingGuidance)

11. Tambahkan juga gitignore pada file atau folder yang tidak perlu di upload, __NB : BINARY TIDAK DIUPLOAD__

12. JSON harus dinormalisasi dan harus di-_preprocessing_
```
Preprocessing contohnya :
- Cleaning
- Parsing
- Transformation
- dan lainnya
```

13. Berikan README yang __WELL DOCUMENTED__ dengan cara __override__ file README.md ini. README harus memuat minimal konten :
```
- Description
- Specification
- How to use
- JSON Structure
- Screenshot program (di-upload pada folder screenshots, di-upload file image nya, dan ditampilkan di dalam README)
- Reference (Library used, etc)
- Author
```
### Dependencies
* Python 3.6
* requests (pip install requests)
* lxml (pip install lxml)
* cssselect (pip install cssselect)

### Usage
Without Makefile
```
scraper.py [--help] [--youtubeid YOUTUBEID] [--outputfile OUTPUTFILE] [--limit LIMIT]
  --help, -h            
                        Getting started with youtube comments scraper
  --youtubeid YOUTUBEID, -y YOUTUBEID
                        ID of Youtube video that we need to scrape
                        https://www.youtube.com/watch?v={youtubeid}
  --outputfile OUTPUTFILE, -o OUTPUTFILE
                        Output filename, end with .json
  --limit LIMIT, -l LIMIT
                        maximum number of comments you want to scrape, do not
                        use it if you want to scrape all comments
```

With Makefile (linux only)
```
python3 src/scraper.py --y youtubeid --o outputfilename
- if necessary, change file directory
- replace youtubeid and outputfilename with Youtube video ID and output filename with extension .json 
```

### JSON Structure
The result will be saved to <outputfilename> with the following format :

```
{
    "cid": Comment ID,
    "text": Comment Content,
    "time": Comment Published Time,
    "author": Comment Author
}
```

### Screenshot
![alt_text]https://github.com/shintaayuck/Seleksi-2018/blob/master/Tugas1/screenshots/Hasil.png


<h1 align="center">
  <br>
  Selamat BerEksplorasi!
  <br>
  <br>
</h1>

### Reference
Library used :
* requests (http://docs.python-requests.org/en/master/)
* lxml (http://lxml.de/)
* cssselect (https://cssselect.readthedocs.io/en/latest/)

### Author
Name : Shinta Ayu CK
Contact : shintaayuck@gmail.com

<p align="center">
  <br>
  Basdat Industries - Lab Basdat 2018
  <br>
  <br>
</p>
