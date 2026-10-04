Nama : Ahmad Rafa Robyan

NPM : 2506620721

Kelas : PBP B

A new update!

### Tugas 1

1. Elemen-elemen tersebut sangat berguna sekali karena dapat memudahkan para developer untuk menyusun struktur design web yang sesuai dan rapi.
2. Beberapa tantangan yang saya harus hadapi untuk membuat web portofolio saya responsif adalah menentukan kalkulasi yang sesuai agar web tetap terlihat rapi dimanapun user mengaksesnya.
3. Karena ini masih web statis, tentunya banyak sekali hal-hal yang belom bisa saya implementasi, salah satunya mungkin sebuah easter-egg minigame yang dapat dimainkan oleh user, sehingga kedepannya saya kepikiran untuk menambahkan hal tersebut ke web portofolio saya.

### Tugas 2

1. urls.py pada proyek merupakan arahan url yang akan menjadi titik universal suatu app yang menggunakan project tersebut, sedangkan urls.py pada app dapat berbeda-beda sesuai dengan ketentuan yang disediakan oleh masing-masing app.
2. Penggunaan models pada portofolio agar membuat pengolahan data menjadi lebih mudah dan praktis karena tidak perlu mencari section pada file html website, serta hal ini memudahkan dalam hal pengolahan data berupa penghapusan maupun perubahan data tanpa merubah aspek
html dari web tersebut.
3. ```makemigrations``` digunakan untuk menginisiasi perubahan-perubahan yang telah dilakukan namun tidak secara langsung mengaplikasikannya ke web, sementara ```migrate``` mengeksekusi file migrasi yang telah dibuat dan diterapkan pada web yang telah kita kembangkan.

### Tugas 3

1. Penggunaan ModelForm yang disedikan oleh Django menjadi hal yang sangat berguna karena dapat memudahkan proses pembuatan form yang nantinya langsung dapat digunakan pada website yang sedang kita buat, sementara csrf token merupakan suatu pencegahan dari hal yang bernama
*Cross Site Request Forgery* yang kurang lebih merupakan tindakan yang meliputi akses terhadap data korban yang nantinya dapat disalahgunakan oleh pihak pelaku yang melakukan hal tersebut, csrf token berguna agar kejadian tersebut dapat dicegah sebelum berdampak pada yang
menjadi korban.
2. JSON lebih banyak digunakan dari pada XML karena beberapa faktor, yang pertama adalah kecepatan, kemudian secara *readability*, JSON dapat lebih mudah untuk dibaca dari pada XML serta kompabilitas secara langsung dengan JavaScript dapat memudahkan implementasi API pada
website yang dikehendaki.
3. Model Django pada titik terdalamnya merupakan sebuah objek yang rumit sehingga tidak dapat dipahami oleh framework yang lain, sehingga *serialization* dilakukan untuk mengubah objek Django tersebut menjadi bagian-bagian queryset yang nantinya dapat diubah menjadi data
JSON yang dapat digunakan atau sebaliknya dari JSON menjadi objek yang rumit dan digunakan kembali.

### Tugas 5
1. Debouncing adalah teknik yang dilakukan agar respons web terlihat seamless, contohnya pada tugas web ini, ketika kita mulai mengetik pada search bar, maka secara langsung nanti akan mem-fetch project dengan nama tersebut dan langsung menampilkannya tanpa harus mereload halaman.
2. await pada fetch() berfungsi sebagai penahan agar kode tidak langsung mengeksekusi kode yang mungkin belom memiliki nilai sepenuhnya, seperti pada contoh fetch data dari Django, jika tidak memakai await maka akan ada kemungkinan data yang ingin diperlihatkan belum siap untuk ditampilkan sehingga menghasilkan error.
3. XSS kurang lebih adalah injeksi sebuah kode JavaScript pada suatu web melalui celah keamananan, hal ini lebih rentan pada web yang menerapkan data dengan AJAX dari pada Django karena input yang masukan tidak akan dilakukan escaping atau pembersihan input, berbeda dengan Django yang sudah built-in mengimplementasikan teknik escaping untuk mencegah hal tersebut terjadi.

AI DISCLOSURE:

- Saya menggunakan Gemini untuk mencari tahu terkait dengan syntax-syntax css yang saya belum sepenuhnya pahami.
- Saya juga menggunakan pallete generator untuk mendapatkan warna yang sesuai dengan apa yang saya inginkan.
- Ada satu error yang memerlukan bantuan AI, saat deploy web porto, ada kasus dimana model Education bagian field ```started_at``` dan ```ended_at``` masih tergolong sebagai timestamp, namun karena model menggunakan PositiveBigIntegerField web akan selalu mereturn 
```ProgrammingError``` karena adanya mismatch data type saat input data, sehingga saya harus menulis beberapa perintah SQL secara langsung untuk menghapus column tersebut dan mengganti nya dengan column yang berbeda tipe.
- Diketahui bahwa halaman project dapat diubah oleh siapa saja, maka dari itu saya mencari tahu dengan AI cara untuk mencegah tersebut, saat ini saya menggunakan decorator login required yang memerlukan akses admin untuk mengakses fitur tambah atau hapus project.
- Tugas 3 mencangkup cukup banyak hal, yakni penerapan CRUD pada semua model yang ada, serta keinginan saya untuk membuat seluruh form dalam bentuk popover ternyata membutuhkan sangat banyak waktu, pada kasus ini saya menggunakan Gemini untuk mempercepat proses kodingan yang meliputi penulisan kode yang berulang, pastinya saya tetap cek terlebih dahulu untuk output yang telah diberikan oleh GenAI sehingga tidak ada error apapun yang nantinya dapat terjadi.
- Sama seperti tugas 3, Tugas 5 ini kurang lebih mengarah pada refaktoring kode yang sudah kita tulis sebelumnya, sehingga penggunanaan GenAI Gemini digunakan untuk mempercepat proses penulisan kode yang kurang lebih sama, hal ini meliputi merubah struktur html yang awalnya Django heavy menjadi struktur AJAX yang sudah ditentukan oleh tutorial, serta generalisasi add_form yang dilakukan juga dihasilkan menggunakan penggunaan Gemini untuk mempercepat penulisan kode.


