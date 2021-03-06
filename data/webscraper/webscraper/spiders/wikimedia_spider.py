import scrapy
from scrapy.utils.url import urljoin_rfc

shortlist = ["Lactarius trivialis","Chlorophyllum olivieri","Clitocybula platyphylla","Flammulaster limulatus","Russula paludosa","Clitocybe nebularis","Boletus edulis","Lactarius vietus","Coprinopsis atramentaria","Amanita vaginata","Cortinarius traganus","Russula foetens","Leccinum aurantiacum","Tricholomopsis decora","Lycoperdon perlatum","Hypholoma capnoides","Chalciporus piperatus","Lactarius fennoscandicus","Suillus luteus","Cortinarius violaceus","Lactarius glyciosmus","Tricholoma portentosum","Russula vinosa","Stropharia aeruginosa","Lactarius aquizonatus","Cortinarius sanguineus","Mycena sanguinolenta","Cortinarius semisanguineus coll.","Rhodocollybia butyracea","Inocybe geophylla","Leccinum holopus","Amanita virosa","Hygrophoropsis aurantiaca","Hydnum repandum","Macrolepiota procera","Tricholoma fulvum","Albatrellus confluens","Gymnopus confluens","Tricholoma matsutake","Hygrophorus agathosmus","Russula emetica","Ramaria boreimaxima","Scleroderma bovista","Agaricus sylvaticus","Lactarius quietus","Boletus reticulatus","Sarcomyxa serotina","Flammulina velutipes coll.","Craterellus tubaeformis","Coprinus comatus","Inocybe rimosa coll.","Cortinarius rubellus","Lepista nuda","Sarcodon scabrosus","Russula xerampelina coll.","Lactarius camphoratus","Lactarius fuliginosus","Russula adusta","Tricholoma virgatum","Tylopilus felleus","Xerocomus subtomentosus coll.","Tapinella atrotomentosa","Lycoperdon pyriforme","Leotia lubrica","Hygrophorus erubescens","Amanita rubescens","Imleria badia","Amanita regalis","Hydnum rufescens coll.","Chroogomphus rutilus coll.","Amanita fulva","Geastrum fimbriatum","Tricholoma stiparophyllum","Pholiota squarrosa","Tricholomopsis rutilans","Hygrocybe punicea","Cortinarius armillatus","Gomphidius roseus","Sarcoscypha austriaca","Hypholoma lateritium","Amanita muscaria","Russula rhodopus","Paxillus involutus","Lepiota cristata","Mutinus ravenelii","Inocybe lacera","Lichenomphalia umbellifera","Mycena galericulata","Armillaria borealis","Tricholoma pessundatum","Lactarius tabidus","Clavariadelphus ligula","Agaricus arvensis","Russula vesca","Lepista sordida","Lactarius aurantiacus","Amanita crocea","Leucocybe connata","Lactarius flexuosus","Marasmius oreades","Bovista nigrescens","Suillus bovinus","Cortinarius mucosus","Armillaria lutea","Ampulloclitocybe clavipes","Lycoperdon excipuliformis","Leccinum variicolor","Lactarius lignyotus","Cuphophyllus pratensis","Sarcodon squamosus","Leccinum vulpinum","Lactarius deliciosus","Boletus pinophilus","Galerina marginata","Hygrophorus camarophyllus","Craterellus cornucopioides","Lactarius turpis","Russula lutea","Cortinarius triumphans","Gomphidius glutinosus","Flammula alnicola","Lactifluus bertillonii","Leccinum populinum","Tricholoma frondosae","Suillus grevillei","Leccinum scabrum coll.","Mycetinis scorodonius","Albatrellus ovinus","Lactarius helvus","Agaricus sylvicola","Ramaria eumorpha","Sarcodon imbricatus","Marasmiellus perforans","Lactarius deterrimus","Strobilurus esculentus","Phaeolepiota aurea","Lactifluus volemus","Craterellus lutescens","Gyromitra esculenta","Leccinum versipelle","Russula intermedia","Kuehneromyces mutabilis","Pluteus cervinus","Russula aeruginea","Hypholoma fasciculare","Clavulinopsis laeticolor","Calocybe gambosa","Phyllotopsis nidulans","Cantharellus cibarius","Hygrocybe chlorophana","Calocera viscosa","Lactarius repraesentaneus","Mitrula paludosa","Mycena epipterygia","Russula claroflava","Cortinarius caperatus","Amanita phalloides","Lactarius torminosus","Morchella elata","Xeromphalina campanella","Suillus variegatus","Lactarius rufus","Lactarius mammosus","Amanita porphyria","Tricholoma equestre","Russula decolorans","Gymnopus dryophilus","Langermannia gigantea","Suillus granulatus","Gymnopus androsaceus","Clitopilus prunulus","Lactarius scrobiculatus"]

class WikimediaSpider(scrapy.Spider):
    name = "wikimedia"
    download_delay = 1.0

    def start_requests(self):
        urls = ["https://commons.wikimedia.org/wiki/%s" % name.lower().replace(" ","_") for name in shortlist]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_mushroom)

    def parse_mushroom(self, response):
        imagepages = response.css("ul.gallery")[0].css("a::attr(href)").getall()
        name_latin = response.url.split("/")[-1].replace("_"," ")
        for imagepage in imagepages:
            yield scrapy.Request(url=str(urljoin_rfc(response.url, imagepage), "ascii"), 
                                 callback=self.parse_imagepage, 
                                 meta={'name_latin' : name_latin})

    def parse_imagepage(self, response):
        url = response.css("img[alt^=File]::attr(src)").get()
        yield { 'name_latin' : response.meta['name_latin'],
                'image_urls' : [url] }