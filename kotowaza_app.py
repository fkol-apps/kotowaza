#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界のことわざアプリ
毎日ひとつ、世界中のことわざをPC画面に表示します。
"""

import tkinter as tk
import tkinter.font
import random
import datetime
import hashlib

# ==========================================
# ことわざデータ（世界60カ国以上から収集）
# ==========================================
PROVERBS = [
    # ─── 日本 ─────────────────────────────
    {"text": "七転び八起き",
     "meaning": "何度失敗しても、そのたびに立ち上がること",
     "country": "日本", "flag": "JP"},

    {"text": "塵も積もれば山となる",
     "meaning": "小さなことでも積み重なれば大きな成果になる",
     "country": "日本", "flag": "JP"},

    {"text": "急がば回れ",
     "meaning": "急ぐときほど、安全で確実な道を選ぶほうがかえって早い",
     "country": "日本", "flag": "JP"},

    {"text": "備えあれば憂いなし",
     "meaning": "準備をしっかりしておけば、いざというときに困らない",
     "country": "日本", "flag": "JP"},

    {"text": "千里の道も一歩から",
     "meaning": "どんな大きな目標も、まず一歩を踏み出すことから始まる",
     "country": "日本", "flag": "JP"},

    {"text": "人事を尽くして天命を待つ",
     "meaning": "できる限りの努力をして、後は天の意志に従う",
     "country": "日本", "flag": "JP"},

    {"text": "三人寄れば文殊の知恵",
     "meaning": "凡人でも三人集まれば、素晴らしい知恵が生まれる",
     "country": "日本", "flag": "JP"},

    {"text": "石の上にも三年",
     "meaning": "辛くても辛抱強く続ければ、必ず報われる",
     "country": "日本", "flag": "JP"},

    {"text": "笑う門には福来たる",
     "meaning": "いつも明るく笑っていれば、幸福がやってくる",
     "country": "日本", "flag": "JP"},

    {"text": "良薬は口に苦し",
     "meaning": "良い忠告や教えは、聞くのがつらいものだ",
     "country": "日本", "flag": "JP"},

    # ─── 中国 ─────────────────────────────
    {"text": "活到老、学到老",
     "meaning": "生きている限り、学び続けよ",
     "country": "中国", "flag": "CN"},

    {"text": "失敗是成功之母",
     "meaning": "失敗は成功の母。失敗から学んでこそ成功がある",
     "country": "中国", "flag": "CN"},

    {"text": "一口吃不成胖子",
     "meaning": "一口では太れない。大きなことも一歩一歩積み上げるもの",
     "country": "中国", "flag": "CN"},

    {"text": "不怕慢、只怕站",
     "meaning": "遅くてもいい、立ち止まることを恐れよ",
     "country": "中国", "flag": "CN"},

    {"text": "路遥知马力，日久见人心",
     "meaning": "長い道のりで馬の力がわかり、長い時間で人の心がわかる",
     "country": "中国", "flag": "CN"},

    # ─── 韓国 ─────────────────────────────
    {"text": "가는 말이 고와야 오는 말이 곱다",
     "meaning": "自分が優しく話せば、相手も優しく返してくれる（言葉は鏡）",
     "country": "韓国", "flag": "KR"},

    {"text": "티끌 모아 태산",
     "meaning": "塵も積もれば山となる。小さな積み重ねが大きな結果を生む",
     "country": "韓国", "flag": "KR"},

    {"text": "세 살 버릇 여든까지 간다",
     "meaning": "三つ子の魂百まで。幼い頃の習慣は老いても続く",
     "country": "韓国", "flag": "KR"},

    # ─── ロシア ────────────────────────────
    {"text": "Бог то бог, да сам не будь плох",
     "meaning": "神を信じよ、しかし自分でもしっかり備えよ",
     "country": "ロシア", "flag": "RU"},

    {"text": "Тише едешь — дальше будешь",
     "meaning": "ゆっくり進む者ほど、遠くまで行ける",
     "country": "ロシア", "flag": "RU"},

    {"text": "Повторение — мать учения",
     "meaning": "繰り返しは学びの母。反復こそが習得への道",
     "country": "ロシア", "flag": "RU"},

    # ─── フランス ──────────────────────────
    {"text": "Après la pluie, le beau temps",
     "meaning": "雨の後には晴れがある。苦労の後には必ず良いことがある",
     "country": "フランス", "flag": "FR"},

    {"text": "Vouloir, c'est pouvoir",
     "meaning": "意志あるところに道あり。強く望めば必ず実現できる",
     "country": "フランス", "flag": "FR"},

    {"text": "L'habit ne fait pas le moine",
     "meaning": "服が修道士を作るわけではない。外見で人を判断するな",
     "country": "フランス", "flag": "FR"},

    {"text": "Petit à petit, l'oiseau fait son nid",
     "meaning": "少しずつ、小鳥は巣を作る。継続こそが大きな成果を生む",
     "country": "フランス", "flag": "FR"},

    # ─── イギリス / アメリカ ────────────────
    {"text": "Every cloud has a silver lining",
     "meaning": "どんな暗い雲にも銀の裏地がある。悪いことにも必ず良い面がある",
     "country": "イギリス", "flag": "GB"},

    {"text": "Actions speak louder than words",
     "meaning": "言葉よりも行動が雄弁に語る",
     "country": "イギリス", "flag": "GB"},

    {"text": "Don't put all your eggs in one basket",
     "meaning": "全ての卵を一つの籠に入れるな。リスクを分散させよ",
     "country": "イギリス", "flag": "GB"},

    {"text": "The early bird catches the worm",
     "meaning": "早起きは三文の得。先手を打つ者が利益を得る",
     "country": "アメリカ", "flag": "US"},

    {"text": "When in Rome, do as the Romans do",
     "meaning": "郷に入っては郷に従え。その土地の習慣に合わせよ",
     "country": "アメリカ", "flag": "US"},

    # ─── ドイツ ────────────────────────────
    {"text": "Übung macht den Meister",
     "meaning": "練習が名人を作る。習うより慣れろ",
     "country": "ドイツ", "flag": "DE"},

    {"text": "Morgenstund hat Gold im Mund",
     "meaning": "朝の時間は金の口を持つ。早起きは三文の得",
     "country": "ドイツ", "flag": "DE"},

    {"text": "Ende gut, alles gut",
     "meaning": "終わりよければすべてよし",
     "country": "ドイツ", "flag": "DE"},

    # ─── スペイン ──────────────────────────
    {"text": "No hay mal que por bien no venga",
     "meaning": "災い転じて福となす。悪いことには必ず良い面がある",
     "country": "スペイン", "flag": "ES"},

    {"text": "A quien madruga, Dios le ayuda",
     "meaning": "早起きする者には神が助けを与える",
     "country": "スペイン", "flag": "ES"},

    {"text": "Camarón que se duerme, se lo lleva la corriente",
     "meaning": "眠るエビは流される。油断していると機会を逃す",
     "country": "メキシコ", "flag": "MX"},

    # ─── イタリア ──────────────────────────
    {"text": "Chi va piano, va sano e va lontano",
     "meaning": "ゆっくり行く者は、安全に遠くまで行ける",
     "country": "イタリア", "flag": "IT"},

    {"text": "A caval donato non si guarda in bocca",
     "meaning": "もらった馬の口を見るな。贈り物に文句を言うな",
     "country": "イタリア", "flag": "IT"},

    # ─── インド ────────────────────────────
    {"text": "जो बोओगे सो काटोगे",
     "meaning": "蒔いた種を刈り取る。自分の行いは自分に返ってくる",
     "country": "インド", "flag": "IN"},

    {"text": "अति सर्वत्र वर्जयेत्",
     "meaning": "何事も過ぎたるは猶及ばざるが如し。何でも適度が大切",
     "country": "インド（サンスクリット）", "flag": "IN"},

    # ─── アラブ ────────────────────────────
    {"text": "الصبر مفتاح الفرج",
     "meaning": "忍耐は解放の鍵。我慢することで道が開ける",
     "country": "アラビア", "flag": "AE"},

    {"text": "الكلام من فضة والصمت من ذهب",
     "meaning": "言葉は銀、沈黙は金。語るよりも黙ることが価値を持つ場合がある",
     "country": "アラビア", "flag": "AE"},

    {"text": "من جد وجد",
     "meaning": "努力する者は必ず得る。勤勉は必ず報われる",
     "country": "アラビア", "flag": "AE"},

    # ─── トルコ ────────────────────────────
    {"text": "Damlaya damlaya göl olur",
     "meaning": "一滴一滴が湖になる。小さな積み重ねが大きな成果を生む",
     "country": "トルコ", "flag": "TR"},

    {"text": "Bugünün işini yarına bırakma",
     "meaning": "今日の仕事を明日に残すな。先延ばしにするな",
     "country": "トルコ", "flag": "TR"},

    # ─── ペルシャ（イラン） ─────────────────
    {"text": "صبر تلخ است ولی میوه شیرین دارد",
     "meaning": "忍耐は苦いが、その果実は甘い",
     "country": "ペルシャ（イラン）", "flag": "IR"},

    {"text": "هر که بامش بیش، برفش بیشتر",
     "meaning": "屋根が大きいほど、雪も多く積もる。地位が高いほど責任も重い",
     "country": "ペルシャ（イラン）", "flag": "IR"},

    # ─── アフリカ ──────────────────────────
    {"text": "Ukweli ni mwanga",
     "meaning": "真実は光。真実を語ることが道を照らす",
     "country": "東アフリカ（スワヒリ語）", "flag": "TZ"},

    {"text": "Haraka haraka haina baraka",
     "meaning": "急いでも幸運は来ない。焦っても良い結果は生まれない",
     "country": "東アフリカ（スワヒリ語）", "flag": "TZ"},

    {"text": "Umuntu ngumuntu ngabantu",
     "meaning": "人は他の人々によって人になる。人は互いのつながりで生きている",
     "country": "南アフリカ（ズールー語）", "flag": "ZA"},

    {"text": "If you want to go fast, go alone. If you want to go far, go together.",
     "meaning": "速く行きたければ一人で行け、遠くへ行きたければ皆で行け",
     "country": "アフリカ", "flag": "AF"},

    {"text": "It takes a village to raise a child",
     "meaning": "子供一人を育てるには村全体が必要。育ちは社会全体の責任",
     "country": "アフリカ（ナイジェリア）", "flag": "NG"},

    # ─── ブラジル / ポルトガル ───────────────
    {"text": "Quem não arrisca, não petisca",
     "meaning": "リスクを冒さない者は何も得られない。挑戦なくして成果なし",
     "country": "ブラジル", "flag": "BR"},

    {"text": "Devagar e sempre",
     "meaning": "ゆっくりと、しかし着実に。焦らずコツコツ続けることが大切",
     "country": "ポルトガル", "flag": "PT"},

    # ─── ノルウェー ────────────────────────
    {"text": "Det finnes ikke dårlig vær, bare dårlige klær",
     "meaning": "悪い天気はない、あるのは悪い服装だけ。準備次第で何でも乗り越えられる",
     "country": "ノルウェー", "flag": "NO"},

    # ─── スウェーデン ──────────────────────
    {"text": "Lagom är bäst",
     "meaning": "ほどほどが一番。何事も適度が最善",
     "country": "スウェーデン", "flag": "SE"},

    # ─── フィンランド ──────────────────────
    {"text": "Työ tekijäänsä kiittää",
     "meaning": "仕事は作者を褒める。誠実に仕事をすれば、それが自分を証明する",
     "country": "フィンランド", "flag": "FI"},

    # ─── ハンガリー ────────────────────────
    {"text": "Lassan járj, tovább érsz",
     "meaning": "ゆっくり行けば、もっと遠くへ行ける",
     "country": "ハンガリー", "flag": "HU"},

    # ─── チェコ ────────────────────────────
    {"text": "Bez práce nejsou koláče",
     "meaning": "働かなければケーキは食べられない。働かざる者食うべからず",
     "country": "チェコ", "flag": "CZ"},

    # ─── オランダ ──────────────────────────
    {"text": "Wie niet waagt, die niet wint",
     "meaning": "挑戦しない者は勝てない",
     "country": "オランダ", "flag": "NL"},

    # ─── ポーランド ────────────────────────
    {"text": "Nie chwal dnia przed zachodem słońca",
     "meaning": "夕日が沈む前に一日を褒めるな。結果が出るまで喜ぶな",
     "country": "ポーランド", "flag": "PL"},

    # ─── ギリシャ ──────────────────────────
    {"text": "Σιγά σιγά πάει μακριά",
     "meaning": "ゆっくりゆっくり遠くへ行く。焦らずじっくりが遠道の近道",
     "country": "ギリシャ", "flag": "GR"},

    # ─── タイ ──────────────────────────────
    {"text": "ไม้อ่อนดัดง่าย ไม้แก่ดัดยาก",
     "meaning": "若い木は曲げやすい、老いた木は曲げにくい。子供のうちに教育せよ",
     "country": "タイ", "flag": "TH"},

    # ─── ベトナム ──────────────────────────
    {"text": "Học ăn, học nói, học gói, học mở",
     "meaning": "食べ方・話し方・包み方・開け方を学べ。礼儀作法すべてが学びの対象",
     "country": "ベトナム", "flag": "VN"},

    # ─── インドネシア ──────────────────────
    {"text": "Bersatu kita teguh, bercerai kita runtuh",
     "meaning": "団結すれば強く、分裂すれば倒れる",
     "country": "インドネシア", "flag": "ID"},

    # ─── モンゴル ──────────────────────────
    {"text": "Нэг үгийн буруу мянган үгийн тайлбараар засдаггүй",
     "meaning": "一言の誤りは千言の説明で直せない。言葉は慎重に選べ",
     "country": "モンゴル", "flag": "MN"},

    # ─── エジプト ──────────────────────────
    {"text": "اللي بيتأخر بياخد العظام",
     "meaning": "遅れる者は骨しかもらえない。早い者勝ちで行動せよ",
     "country": "エジプト", "flag": "EG"},

    # ─── イスラエル ────────────────────────
    {"text": "אם אין אני לי, מי לי",
     "meaning": "もし私が自分のためにならないなら、誰がなるというのか（自助の精神）",
     "country": "イスラエル（ヘブライ語）", "flag": "IL"},

    # ─── フィリピン ────────────────────────
    {"text": "Ang hindi marunong lumingon sa pinanggalingan\nay hindi makakarating sa paroroonan",
     "meaning": "来た道を振り返れない者は、目的地に着けない。自分の過去を大切に",
     "country": "フィリピン", "flag": "PH"},

    # ─── ネパール ──────────────────────────
    {"text": "जहाँ जाउ त्यहाँको बन",
     "meaning": "郷に入っては郷に従え。その土地のルールを尊重せよ",
     "country": "ネパール", "flag": "NP"},

    # ─── アイルランド ──────────────────────
    {"text": "Is fearr Gaeilge briste ná Béarla cliste",
     "meaning": "下手なアイルランド語は巧みな英語より良い。母語への誇りを忘れるな",
     "country": "アイルランド", "flag": "IE"},

    # ─── アルゼンチン ──────────────────────
    {"text": "No hay mal que dure cien años",
     "meaning": "百年続く悪はない。どんな苦難も必ず終わる",
     "country": "アルゼンチン", "flag": "AR"},

    # ─── トルクメニスタン（中央アジア）───────
    {"text": "Sabyr düybünde altyn bar",
     "meaning": "忍耐の底には金がある。辛抱の先に宝がある",
     "country": "中央アジア", "flag": "TM"},

    # ─── スコットランド ────────────────────
    {"text": "Dinnae teach your grandmother to suck eggs",
     "meaning": "祖母に卵の吸い方を教えるな。経験者に基本を教えようとするな",
     "country": "スコットランド", "flag": "GB"},

    {"text": "Mony a mickle maks a muckle",
     "meaning": "小銭が積もれば大金になる。小さな積み重ねを侮るな",
     "country": "スコットランド", "flag": "GB"},

    # ─── アイルランド（追加） ──────────────
    {"text": "Ní neart go cur le chéile",
     "meaning": "協力なくして力なし。団結してこそ強くなれる",
     "country": "アイルランド", "flag": "IE"},

    # ─── ウェールズ ────────────────────────
    {"text": "Heb ei fai, heb ei eni",
     "meaning": "欠点のない者は生まれていない。完璧な人間はいない",
     "country": "ウェールズ", "flag": "GB"},

    # ─── デンマーク ────────────────────────
    {"text": "Den der tier, samtykker",
     "meaning": "黙っている者は同意している。沈黙は肯定のしるし",
     "country": "デンマーク", "flag": "DK"},

    {"text": "Øvelse gør mester",
     "meaning": "練習が名人を作る。継続的な努力が技術を磨く",
     "country": "デンマーク", "flag": "DK"},

    # ─── アイスランド ──────────────────────
    {"text": "Þetta reddast",
     "meaning": "なんとかなる。どうにかなるさというアイスランド人の楽観的精神",
     "country": "アイスランド", "flag": "IS"},

    # ─── スイス ────────────────────────────
    {"text": "Spare in der Zeit, so hast du in der Not",
     "meaning": "豊かなときに節約せよ、そうすれば困ったときにも持つ",
     "country": "スイス（ドイツ語圏）", "flag": "CH"},

    # ─── オーストリア ──────────────────────
    {"text": "Reden ist Silber, Schweigen ist Gold",
     "meaning": "言葉は銀、沈黙は金。語るよりも黙ることが時に価値がある",
     "country": "オーストリア", "flag": "AT"},

    # ─── ベルギー ──────────────────────────
    {"text": "Wie niet werkt, zal niet eten",
     "meaning": "働かない者は食べてはならない。働いてこそ報われる",
     "country": "ベルギー", "flag": "BE"},

    # ─── ルーマニア ────────────────────────
    {"text": "Graba strică treaba",
     "meaning": "急ぎは仕事を台無しにする。焦ると失敗する",
     "country": "ルーマニア", "flag": "RO"},

    {"text": "Omul sfințește locul",
     "meaning": "人が場所を聖なるものにする。人によって場所の価値が決まる",
     "country": "ルーマニア", "flag": "RO"},

    # ─── ウクライナ ────────────────────────
    {"text": "Без труда нема плода",
     "meaning": "苦労なくして果実なし。努力なしに成果は得られない",
     "country": "ウクライナ", "flag": "UA"},

    {"text": "Де згода, там і перемога",
     "meaning": "一致団結するところに勝利がある",
     "country": "ウクライナ", "flag": "UA"},

    # ─── ブルガリア ────────────────────────
    {"text": "Не оставяй за утре това, което можеш да направиш днес",
     "meaning": "今日できることを明日に残すな",
     "country": "ブルガリア", "flag": "BG"},

    # ─── セルビア ──────────────────────────
    {"text": "Слога кућу гради",
     "meaning": "調和が家を建てる。団結が何かを生み出す",
     "country": "セルビア", "flag": "RS"},

    # ─── ジョージア（旧グルジア） ──────────
    {"text": "სტუმარი ღვთის მოვლინებაა",
     "meaning": "客は神の遣い。訪ねてくる人は大切にしなければならない",
     "country": "ジョージア", "flag": "GE"},

    # ─── アルメニア ────────────────────────
    {"text": "Ծառը, որ ծաղիկ չի տալիս, ստվեր չի տալիս",
     "meaning": "花を咲かせない木は陰を作れない。与えない者は守れない",
     "country": "アルメニア", "flag": "AM"},

    # ─── アゼルバイジャン ──────────────────
    {"text": "Ağac meyvəsindən tanınar",
     "meaning": "木はその実でわかる。人はその行いで知られる",
     "country": "アゼルバイジャン", "flag": "AZ"},

    # ─── カザフスタン ──────────────────────
    {"text": "Жеті рет өлшеп, бір рет кес",
     "meaning": "七回測って一回切れ。慎重に考えてから行動せよ",
     "country": "カザフスタン", "flag": "KZ"},

    # ─── ウズベキスタン ────────────────────
    {"text": "Bilim — nur, bilmaslik — qorong'ulik",
     "meaning": "知識は光、無知は闇",
     "country": "ウズベキスタン", "flag": "UZ"},

    # ─── アフガニスタン ────────────────────
    {"text": "کار نیک را کن و در آب انداز",
     "meaning": "良いことをして、川に流せ。見返りを求めずに善行をせよ",
     "country": "アフガニスタン", "flag": "AF"},

    # ─── パキスタン ────────────────────────
    {"text": "صبر کا پھل میٹھا ہوتا ہے",
     "meaning": "忍耐の果実は甘い。辛抱すれば良いことがある",
     "country": "パキスタン（ウルドゥー語）", "flag": "PK"},

    # ─── スリランカ ────────────────────────
    {"text": "ඉවසීම ජය ගනී",
     "meaning": "忍耐は勝利する。辛抱強さが最終的に勝つ",
     "country": "スリランカ（シンハラ語）", "flag": "LK"},

    # ─── ミャンマー ────────────────────────
    {"text": "ကြိုးစားမှ ကြိုးပမ်းနိုင်",
     "meaning": "努力してこそ達成できる",
     "country": "ミャンマー", "flag": "MM"},

    # ─── カンボジア ────────────────────────
    {"text": "ដំបូងគិត ក្រោយនិយាយ",
     "meaning": "まず考えて、それから話せ。口より先に頭を使え",
     "country": "カンボジア（クメール語）", "flag": "KH"},

    # ─── マレーシア ────────────────────────
    {"text": "Seperti menatang minyak yang penuh",
     "meaning": "満杯の油を運ぶように大切に扱え。慎重さと敬意を忘れるな",
     "country": "マレーシア", "flag": "MY"},

    {"text": "Tak kenal maka tak cinta",
     "meaning": "知らなければ愛せない。理解することが愛の始まり",
     "country": "マレーシア", "flag": "MY"},

    # ─── チベット ──────────────────────────
    {"text": "མི་ལ་གཅིག་གིས་ཕན་ཐོགས་བྱེད་ན་སྐྱེ་བ་ཡིག་པར་འགྱུར",
     "meaning": "一人が他の人を助けることができれば、その生は意味を持つ",
     "country": "チベット", "flag": "CN"},

    # ─── 台湾 ──────────────────────────────
    {"text": "吃苦耐勞",
     "meaning": "苦しみを食べ、労苦に耐える。困難に耐え忍ぶことを厭わない精神",
     "country": "台湾", "flag": "TW"},

    # ─── モロッコ（追加） ──────────────────
    {"text": "العجلة من الشيطان والتأني من الرحمن",
     "meaning": "急ぎは悪魔から、慎重さは神から。焦りは失敗のもと",
     "country": "モロッコ", "flag": "MA"},

    # ─── チュニジア ────────────────────────
    {"text": "من صبر ظفر",
     "meaning": "辛抱した者は成功する",
     "country": "チュニジア", "flag": "TN"},

    # ─── エチオピア ────────────────────────
    {"text": "እሳት ሲጠጉ ያሞቃል ሲርቁ ያቀዘቅዛል",
     "meaning": "火は近くにいれば温め、離れれば冷たくなる。関係は距離で変わる",
     "country": "エチオピア", "flag": "ET"},

    {"text": "Yetebaberut lijoch ahiya ayidarum",
     "meaning": "一緒に育った子供たちは、ロバでも引き倒せない。仲間の絆は強い",
     "country": "エチオピア", "flag": "ET"},

    # ─── ガーナ ────────────────────────────
    {"text": "Obra ye Obi Ntoma",
     "meaning": "人生は他人の服。誰も他人の人生を完全に理解はできない",
     "country": "ガーナ（アカン語）", "flag": "GH"},

    {"text": "Onipa na ohia onipa",
     "meaning": "人は人を必要とする。誰もが誰かを必要としている",
     "country": "ガーナ", "flag": "GH"},

    # ─── セネガル ──────────────────────────
    {"text": "Jëf ak xam-xam dafa am solo",
     "meaning": "行動と知識の両方が価値を持つ",
     "country": "セネガル（ウォロフ語）", "flag": "SN"},

    # ─── マダガスカル ──────────────────────
    {"text": "Ny fiainana toy ny ala: aleo aloha ny hatsaram-panahy",
     "meaning": "人生は森のよう。まず親切心を前に出せ",
     "country": "マダガスカル", "flag": "MG"},

    # ─── コロンビア ────────────────────────
    {"text": "El que madruga, Dios le ayuda",
     "meaning": "早起きする者には神が助けを与える",
     "country": "コロンビア", "flag": "CO"},

    {"text": "A mal tiempo, buena cara",
     "meaning": "悪い天気には良い顔を。困難の中でも笑顔でいよ",
     "country": "コロンビア", "flag": "CO"},

    # ─── ペルー ────────────────────────────
    {"text": "El que no llora, no mama",
     "meaning": "泣かない者は乳を飲めない。積極的に求めなければ得られない",
     "country": "ペルー", "flag": "PE"},

    # ─── チリ ──────────────────────────────
    {"text": "Camarón que se duerme, se lo lleva la corriente",
     "meaning": "眠れば流される。油断すると機会を失う",
     "country": "チリ", "flag": "CL"},

    # ─── キューバ ──────────────────────────
    {"text": "El muerto y el arrimado a los tres días apestan",
     "meaning": "死者も居候も三日で臭くなる。客は三日で臭くなる",
     "country": "キューバ", "flag": "CU"},

    # ─── ジャマイカ ────────────────────────
    {"text": "Every mickle mek a muckle",
     "meaning": "一つ一つが積み重なって大きくなる。小さなことを大切に",
     "country": "ジャマイカ", "flag": "JM"},

    # ─── ハイチ ────────────────────────────
    {"text": "Deye mòn gen mòn",
     "meaning": "山の向こうにまた山がある。一つの困難を乗り越えても次がある",
     "country": "ハイチ", "flag": "HT"},

    # ─── オーストラリア ────────────────────
    {"text": "No worries, mate",
     "meaning": "心配するな、大丈夫。楽観的に物事を捉えよ",
     "country": "オーストラリア", "flag": "AU"},

    # ─── マオリ（ニュージーランド） ───────────
    {"text": "He aha te mea nui o te ao? He tangata, he tangata, he tangata",
     "meaning": "世界で最も大切なものは何か？人、人、人だ",
     "country": "マオリ（ニュージーランド）", "flag": "NZ"},

    {"text": "Whāia te iti kahurangi ki te tūohu koe me he maunga teitei",
     "meaning": "高い目標を持て。もし頭を垂れるなら、それは高い山のように",
     "country": "マオリ（ニュージーランド）", "flag": "NZ"},

    # ─── カナダ（ケベック） ────────────────
    {"text": "Vouloir, c'est pouvoir, mais pouvoir n'est pas toujours vouloir",
     "meaning": "意志は力になる。しかし力があっても意志がなければ動けない",
     "country": "カナダ（ケベック）", "flag": "CA"},

    # ─── ネイティブ・アメリカン ────────────
    {"text": "We do not inherit the earth from our ancestors;\nwe borrow it from our children",
     "meaning": "私たちは大地を祖先から受け継いだのではない。子供たちから借りているのだ",
     "country": "ネイティブ・アメリカン", "flag": "US"},

    {"text": "Don't judge a man until you have walked two moons in his moccasins",
     "meaning": "その人の靴で二か月歩くまで、人を裁くな。相手の立場を理解せよ",
     "country": "ネイティブ・アメリカン（チェロキー族）", "flag": "US"},

    # ─── リトアニア ────────────────────────
    {"text": "Kiek žmonių, tiek nuomonių",
     "meaning": "人の数だけ意見がある。十人十色",
     "country": "リトアニア", "flag": "LT"},

    # ─── ラトビア ──────────────────────────
    {"text": "Kā sauc, tā atbild",
     "meaning": "呼ぶように、応じる。自分の言葉は返ってくる",
     "country": "ラトビア", "flag": "LV"},

    # ─── エストニア ────────────────────────
    {"text": "Töö kiidab tegijat",
     "meaning": "仕事が作者を褒める。仕事の質が人を語る",
     "country": "エストニア", "flag": "EE"},

    # ─── スロバキア ────────────────────────
    {"text": "Bez práce nie sú koláče",
     "meaning": "働かなければケーキは食べられない。努力なくして成果なし",
     "country": "スロバキア", "flag": "SK"},

    # ─── クロアチア ────────────────────────
    {"text": "Bolje spriječiti nego liječiti",
     "meaning": "治療より予防の方が良い。後悔する前に備えよ",
     "country": "クロアチア", "flag": "HR"},

    # ─── バスク地方 ────────────────────────
    {"text": "Nahi duena ari da, nahi ez duena arrazoia bilatzen",
     "meaning": "やりたい者はやる、やりたくない者は言い訳を探す",
     "country": "バスク地方（スペイン）", "flag": "ES"},

    # ─── ベトナム（追加） ─────────────────
    {"text": "Có công mài sắt, có ngày nên kim",
     "meaning": "鉄を磨き続ければ、いつか針になる。継続は力なり",
     "country": "ベトナム", "flag": "VN"},

    # ─── タイ（追加） ─────────────────────
    {"text": "น้ำขึ้นให้รีบตัก",
     "meaning": "水が上がったときにすくえ。チャンスが来たら逃すな",
     "country": "タイ", "flag": "TH"},

    # ─── 中国（追加） ─────────────────────
    {"text": "书山有路勤为径，学海无涯苦作舟",
     "meaning": "知識の山には勤勉という道があり、学問の海には苦労という舟がある",
     "country": "中国", "flag": "CN"},

    {"text": "知己知彼，百战百胜",
     "meaning": "己を知り敵を知れば百戦百勝。自分と相手をよく知れば必ず勝てる",
     "country": "中国（孫子）", "flag": "CN"},

    # ─── 日本（追加） ─────────────────────
    {"text": "継続は力なり",
     "meaning": "続けることそのものが力となる",
     "country": "日本", "flag": "JP"},

    {"text": "明日は明日の風が吹く",
     "meaning": "先のことはわからないが、なるようになる。今日は今日のことをすればいい",
     "country": "日本", "flag": "JP"},

    {"text": "負けるが勝ち",
     "meaning": "あえて負けてやることが、長い目で見ると勝ちになることがある",
     "country": "日本", "flag": "JP"},

    {"text": "郷に入っては郷に従え",
     "meaning": "その土地や集団に入ったら、そこのやり方や慣習に従うべき",
     "country": "日本", "flag": "JP"},

    {"text": "転んでもただでは起きない",
     "meaning": "失敗しても必ず何か利益を得ようとする、たくましい精神",
     "country": "日本", "flag": "JP"},

    # ─── ロシア（追加） ────────────────────
    {"text": "Не всё то золото, что блестит",
     "meaning": "輝くものがすべて金ではない。外見に惑わされるな",
     "country": "ロシア", "flag": "RU"},

    {"text": "Утро вечера мудренее",
     "meaning": "朝は夕より賢い。一晩寝れば知恵が出る",
     "country": "ロシア", "flag": "RU"},

    # ─── アラビア（追加） ─────────────────
    {"text": "العقل زينة",
     "meaning": "知性は美しさ。頭の良さこそが真の美",
     "country": "アラビア", "flag": "AE"},

    {"text": "اضرب حديدك وهو حامٍ",
     "meaning": "熱いうちに鉄を打て。チャンスを逃すな",
     "country": "アラビア", "flag": "AE"},

    # ─── インド（追加） ────────────────────
    {"text": "करत करत अभ्यास के, जड़मति होत सुजान",
     "meaning": "繰り返し練習すれば、鈍い者も賢くなる。努力に勝る才能なし",
     "country": "インド（ヒンディー語）", "flag": "IN"},

    # ─── スペイン（追加） ─────────────────
    {"text": "Más vale tarde que nunca",
     "meaning": "遅れても来ないよりまし。遅くてもやらないよりやる方が良い",
     "country": "スペイン", "flag": "ES"},

    {"text": "Al que madruga, Dios le ayuda",
     "meaning": "早起きする者には神が助けを与える",
     "country": "スペイン", "flag": "ES"},

    # ─── イギリス（追加） ─────────────────
    {"text": "A stitch in time saves nine",
     "meaning": "今一針縫えば後で九針縫わずに済む。早めの対処が大切",
     "country": "イギリス", "flag": "GB"},

    {"text": "The pen is mightier than the sword",
     "meaning": "ペンは剣よりも強し。言葉や文章の力は武力より大きい",
     "country": "イギリス", "flag": "GB"},

    # ─── アメリカ（追加） ─────────────────
    {"text": "If you can dream it, you can do it",
     "meaning": "夢見ることができれば、それは実現できる",
     "country": "アメリカ", "flag": "US"},

    # ─── イタリア（追加） ─────────────────
    {"text": "Non tutte le ciambelle riescono col buco",
     "meaning": "すべてのドーナツに穴があくわけではない。物事が常にうまくいくとは限らない",
     "country": "イタリア", "flag": "IT"},

    # ─── ドイツ（追加） ────────────────────
    {"text": "Aller Anfang ist schwer",
     "meaning": "すべての始まりは難しい。最初の一歩が一番つらい",
     "country": "ドイツ", "flag": "DE"},

    # ─── フランス（追加） ─────────────────
    {"text": "Les absents ont toujours tort",
     "meaning": "不在者は常に間違っている。その場にいなければ弁解できない",
     "country": "フランス", "flag": "FR"},

    # ─── トルコ（追加） ────────────────────
    {"text": "İşleyen demir pas tutmaz",
     "meaning": "動く鉄は錆びない。活動し続ける者は衰えない",
     "country": "トルコ", "flag": "TR"},

    # ─── ナイジェリア（追加） ─────────────
    {"text": "Bi omi ba pọ, eja a pọ",
     "meaning": "水が多いところに魚が集まる。豊かなところに人が集まる",
     "country": "ナイジェリア（ヨルバ語）", "flag": "NG"},

    # ─── 東アフリカ（追加） ───────────────
    {"text": "Damu nzito kuliko maji",
     "meaning": "血は水より濃い。家族の絆は他の何よりも強い",
     "country": "東アフリカ（スワヒリ語）", "flag": "TZ"},

    # ─── ブータン ──────────────────────────
    {"text": "རྒྱལ་ཁམས་ཀྱི་དགའ་སྐྱིད་ནི་མི་མང་གི་དགའ་སྐྱིད་ཡིན།",
     "meaning": "国の幸福は国民の幸福にある。GNH（国民総幸福量）の精神",
     "country": "ブータン", "flag": "BT"},

    # ─── 日本（追加）────────────────────────
    {"text": "虎穴に入らずんば虎子を得ず",
     "meaning": "危険を冒さなければ、大きな成果は得られない",
     "country": "日本", "flag": "JP"},

    {"text": "猿も木から落ちる",
     "meaning": "どんな名人でも失敗することがある。驕らず謙虚でいよ",
     "country": "日本", "flag": "JP"},

    {"text": "花より団子",
     "meaning": "風情よりも実利を好む。見た目より中身が大切",
     "country": "日本", "flag": "JP"},

    {"text": "知らぬが仏",
     "meaning": "知らないでいる方が、かえって穏やかでいられることがある",
     "country": "日本", "flag": "JP"},

    {"text": "門前の小僧習わぬ経を読む",
     "meaning": "日常的に触れていれば、自然と身につくことがある",
     "country": "日本", "flag": "JP"},

    {"text": "一石二鳥",
     "meaning": "一つの行動で二つの利益を得る",
     "country": "日本", "flag": "JP"},

    {"text": "棚からぼた餅",
     "meaning": "思いがけない幸運が突然やってくること",
     "country": "日本", "flag": "JP"},

    {"text": "目は口ほどにものを言う",
     "meaning": "目は言葉と同じくらい多くのことを伝える",
     "country": "日本", "flag": "JP"},

    {"text": "身から出た錆",
     "meaning": "自分の行いが招いた悪い結果は、自分で引き受けるしかない",
     "country": "日本", "flag": "JP"},

    # ─── 中国（追加）────────────────────────
    {"text": "一分耕耘，一分收获",
     "meaning": "耕した分だけ収穫できる。努力した分だけ結果が出る",
     "country": "中国", "flag": "CN"},

    {"text": "三人行，必有我师焉",
     "meaning": "三人旅をすれば、必ず自分の師となる人がいる",
     "country": "中国（孔子）", "flag": "CN"},

    {"text": "欲速则不达",
     "meaning": "急ぎすぎると目標に達しない。焦りは禁物",
     "country": "中国", "flag": "CN"},

    {"text": "工欲善其事，必先利其器",
     "meaning": "仕事をうまくやろうとすれば、まず道具を整えよ。準備が大切",
     "country": "中国", "flag": "CN"},

    {"text": "吃一堑，长一智",
     "meaning": "一度失敗すれば、一つ賢くなる。失敗から学べ",
     "country": "中国", "flag": "CN"},

    # ─── 韓国（追加）────────────────────────
    {"text": "하늘이 무너져도 솟아날 구멍이 있다",
     "meaning": "天が崩れても逃げ穴がある。どんな絶望的な状況にも必ず活路がある",
     "country": "韓国", "flag": "KR"},

    {"text": "공든 탑이 무너지랴",
     "meaning": "努力して築いた塔は崩れない。誠実な努力は必ず報われる",
     "country": "韓国", "flag": "KR"},

    {"text": "백지장도 맞들면 낫다",
     "meaning": "一枚の紙も二人で持てば楽になる。協力の大切さ",
     "country": "韓国", "flag": "KR"},

    {"text": "말이 씨가 된다",
     "meaning": "言葉は種になる。口に出したことは実現することがある",
     "country": "韓国", "flag": "KR"},

    # ─── ブラジル／ポルトガル（追加）──────────
    {"text": "A pressa é inimiga da perfeição",
     "meaning": "急ぎは完璧の敵。焦ると仕事が雑になる",
     "country": "ブラジル", "flag": "BR"},

    {"text": "Quem tem boca vai a Roma",
     "meaning": "口のある者はローマへも行ける。聞くことを恐れるな",
     "country": "ポルトガル", "flag": "PT"},

    {"text": "Água mole em pedra dura tanto bate até que fura",
     "meaning": "柔らかい水でも硬い岩に打ち続ければ穴が開く。継続の力",
     "country": "ブラジル", "flag": "BR"},

    # ─── スペイン／ラテンアメリカ（追加）────────
    {"text": "No se ganó Zamora en una hora",
     "meaning": "サモラは一時間で征服されなかった。大きなことは時間がかかる",
     "country": "スペイン", "flag": "ES"},

    {"text": "A caballo regalado no le mires el diente",
     "meaning": "もらった馬の歯を見るな。贈り物に文句を言うな",
     "country": "スペイン", "flag": "ES"},

    {"text": "Dime con quién andas y te diré quién eres",
     "meaning": "誰と歩くかを言えば、あなたが誰かわかる。付き合う人で人柄がわかる",
     "country": "スペイン", "flag": "ES"},

    {"text": "Del dicho al hecho hay un gran trecho",
     "meaning": "言うことと行うことの間には大きな隔たりがある",
     "country": "メキシコ", "flag": "MX"},

    {"text": "Pueblo unido jamás será vencido",
     "meaning": "団結した民は決して征服されない",
     "country": "チリ", "flag": "CL"},

    # ─── アフリカ（追加）────────────────────
    {"text": "Sticks in a bundle are unbreakable",
     "meaning": "束になった枝は折れない。団結の力は偉大だ",
     "country": "ケニア", "flag": "KE"},

    {"text": "A child who is not embraced by the village\nwill burn it down to feel its warmth",
     "meaning": "村に受け入れられない子供は温もりを求めて村を燃やす。社会の包容力の大切さ",
     "country": "アフリカ", "flag": "NG"},

    {"text": "Until the lion learns to write,\nevery story will glorify the hunter",
     "meaning": "ライオンが書くことを学ぶまで、すべての物語はハンターを称える。語る者が歴史を作る",
     "country": "アフリカ", "flag": "NG"},

    {"text": "Do not look where you fell, but where you slipped",
     "meaning": "倒れた場所ではなく、滑った場所を見よ。失敗の原因を探れ",
     "country": "ガーナ", "flag": "GH"},

    {"text": "Rain does not fall on one roof alone",
     "meaning": "雨は一つの屋根だけに降るのではない。喜びも苦しみも分かち合うもの",
     "country": "カメルーン", "flag": "CM"},

    {"text": "However long the night, the dawn will break",
     "meaning": "夜がどれほど長くても、夜明けは来る",
     "country": "マリ", "flag": "ML"},

    # ─── 中東・南アジア（追加）──────────────
    {"text": "يد واحدة لا تصفق",
     "meaning": "片手では拍手できない。何事も協力が必要",
     "country": "アラビア", "flag": "AE"},

    {"text": "إذا أردت أن تعرف رجلا فانظر إلى صديقه",
     "meaning": "人を知りたければ、その友人を見よ。友人は人格を映す鏡",
     "country": "アラビア", "flag": "AE"},

    {"text": "من عاشر القوم أربعين يوما صار منهم",
     "meaning": "四十日間人々と共にいれば、その一員になる。環境が人を形成する",
     "country": "モロッコ", "flag": "MA"},

    {"text": "آینه عیب رو نشان می‌دهد",
     "meaning": "鏡は欠点を映す。真実は時に耳の痛いことを告げる",
     "country": "ペルシャ（イラン）", "flag": "IR"},

    {"text": "جو بوئی، همان دروی",
     "meaning": "蒔いた種を刈り取る。自分の行いは自分に返ってくる",
     "country": "ペルシャ（イラン）", "flag": "IR"},

    {"text": "जल्दी का काम शैतान का",
     "meaning": "急いでする仕事は悪魔のもの。焦りは失敗を招く",
     "country": "インド（ヒンディー語）", "flag": "IN"},

    {"text": "अकेला चना भाड़ नहीं फोड़ सकता",
     "meaning": "一粒のひよこ豆では鍋は割れない。一人の力には限界がある",
     "country": "インド（ヒンディー語）", "flag": "IN"},

    # ─── 東南アジア（追加）──────────────────
    {"text": "น้ำเย็นใจ",
     "meaning": "心を冷たい水のように保て。冷静さを失うな",
     "country": "タイ", "flag": "TH"},

    {"text": "Malakí man ang dagat, maliliit pa rin ang alon",
     "meaning": "海がどれほど大きくても、波は小さくなることがある。謙虚さを忘れるな",
     "country": "フィリピン", "flag": "PH"},

    {"text": "Adat bersendi syarak, syarak bersendi kitabullah",
     "meaning": "慣習は宗教的戒律に根ざし、戒律は聖典に根ざす。根を大切に",
     "country": "マレーシア", "flag": "MY"},

    {"text": "Di mana bumi dipijak, di situ langit dijunjung",
     "meaning": "踏みしめる地に、天を仰げ。その土地を尊重せよ",
     "country": "インドネシア", "flag": "ID"},

    {"text": "Ving gạo ba năm được bữa cơm",
     "meaning": "三年米をつけば一膳の飯になる。積み重ねの大切さ",
     "country": "ベトナム", "flag": "VN"},

    # ─── 北欧（追加）────────────────────────
    {"text": "Sisu",
     "meaning": "どんな困難にも諦めずに立ち向かう強靭な意志と忍耐力（フィンランド特有の精神）",
     "country": "フィンランド", "flag": "FI"},

    {"text": "Man ska inte kasta sten i glashus",
     "meaning": "ガラスの家に石を投げるな。自分の欠点を棚に上げて人を批判するな",
     "country": "スウェーデン", "flag": "SE"},

    {"text": "Livet er ikke en dans på roser",
     "meaning": "人生はバラの上でのダンスではない。人生は楽なものではない",
     "country": "デンマーク", "flag": "DK"},

    # ─── 東欧（追加）────────────────────────
    {"text": "Не рубят лес, так и щепки не летят",
     "meaning": "木を切らなければ木くずは飛ばない。何もしなければリスクもない",
     "country": "ロシア", "flag": "RU"},

    {"text": "За двумя зайцами погонишься — ни одного не поймаешь",
     "meaning": "二匹の兎を追う者は一匹も捕まえられない。欲張ると何も得られない",
     "country": "ロシア", "flag": "RU"},

    {"text": "Не место красит человека, а человек место",
     "meaning": "場所が人を飾るのではなく、人が場所を飾る。人の在り方が大切",
     "country": "ロシア", "flag": "RU"},

    {"text": "Добре тому, хто в своїй хаті",
     "meaning": "自分の家にいる者は幸せ。我が家が一番",
     "country": "ウクライナ", "flag": "UA"},

    {"text": "Ahol nincs meg a régi, ott az új sem terem",
     "meaning": "古いものがなければ、新しいものも生まれない。伝統と革新",
     "country": "ハンガリー", "flag": "HU"},

    # ─── 中央アジア（追加）──────────────────
    {"text": "Mehman xudoning mehmonídir",
     "meaning": "客は神の客である。来訪者を手厚くもてなせ",
     "country": "ウズベキスタン", "flag": "UZ"},

    {"text": "Bir qo'lning ovozi chiqmaydi",
     "meaning": "一本の手では音は出ない。協力してこそ声が届く",
     "country": "ウズベキスタン", "flag": "UZ"},

    {"text": "Ата жұрт — алтын бесік",
     "meaning": "父祖の地は黄金の揺りかご。故郷は何より大切",
     "country": "カザフスタン", "flag": "KZ"},

    # ─── オセアニア（追加）──────────────────
    {"text": "Ehara tāku toa i te toa takitahi, engari he toa takimano",
     "meaning": "私の強さは一人の戦士の強さではなく、千人の戦士の強さだ",
     "country": "マオリ（ニュージーランド）", "flag": "NZ"},

    {"text": "Slow down and the thing you are chasing\nwill come around and catch you",
     "meaning": "ゆっくり進めば、追っているものがあなたを追いかけてくる",
     "country": "オーストラリア（アボリジニ）", "flag": "AU"},

    # ─── 北米（追加）────────────────────────
    {"text": "When you were born, you cried and the world rejoiced.\nLive your life so that when you die,\nthe world cries and you rejoice.",
     "meaning": "生まれた時、あなたは泣き世界は喜んだ。死ぬ時には世界が泣きあなたが喜ぶような人生を生きよ",
     "country": "ネイティブ・アメリカン", "flag": "US"},

    {"text": "Hold on to what is good, even if it is a handful of earth",
     "meaning": "良いものはたとえ一握りの土でも大切に持ち続けよ",
     "country": "ネイティブ・アメリカン（プエブロ族）", "flag": "US"},

    # ─── 日本（さらに追加）────────────────────
    {"text": "情けは人の為ならず",
     "meaning": "人に親切にすることは、巡り巡って自分のためになる",
     "country": "日本", "flag": "JP"},

    {"text": "井の中の蛙大海を知らず",
     "meaning": "狭い世界しか知らず、広い世界を知らないこと。常に視野を広げよ",
     "country": "日本", "flag": "JP"},

    {"text": "一期一会",
     "meaning": "一生に一度の出会い。今この瞬間を大切にせよ",
     "country": "日本", "flag": "JP"},

    {"text": "百聞は一見に如かず",
     "meaning": "百回聞くよりも、一度実際に見た方が確かだ",
     "country": "日本", "flag": "JP"},

    {"text": "案ずるより産むが易し",
     "meaning": "あれこれ心配するより、実際にやってみた方が意外と簡単なもの",
     "country": "日本", "flag": "JP"},

    {"text": "初心忘るべからず",
     "meaning": "何事も始めた頃の謙虚な気持ちや情熱を忘れてはいけない",
     "country": "日本", "flag": "JP"},

    {"text": "光陰矢の如し",
     "meaning": "時間はあっという間に過ぎ去る。大切に使え",
     "country": "日本", "flag": "JP"},

    {"text": "好きこそものの上手なれ",
     "meaning": "好きなことに情熱を持って取り組むと、自然と上達する",
     "country": "日本", "flag": "JP"},

    {"text": "二兎を追う者は一兎をも得ず",
     "meaning": "二つのことを同時に追うと、どちらも得られない",
     "country": "日本", "flag": "JP"},

    {"text": "雨降って地固まる",
     "meaning": "争いや困難があった後は、かえって関係や物事が安定する",
     "country": "日本", "flag": "JP"},

    {"text": "出る杭は打たれる",
     "meaning": "目立つ人や優れた才能を持つ人は、妬まれ妨害されやすい",
     "country": "日本", "flag": "JP"},

    {"text": "柳に雪折れなし",
     "meaning": "柔らかく柔軟であることが、かえって強さとなる",
     "country": "日本", "flag": "JP"},

    # ─── 古代ローマ（ラテン語）────────────────
    {"text": "Carpe diem",
     "meaning": "その日を摘め。今この瞬間を大切に生きよ",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "Per aspera ad astra",
     "meaning": "困難を通じて星へ。苦労の果てに栄光がある",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "Tempus fugit",
     "meaning": "時は飛ぶ。時間はあっという間に過ぎ去る",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "Dum spiro, spero",
     "meaning": "息がある限り、希望がある。生きている限りあきらめるな",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "Fortes fortuna adiuvat",
     "meaning": "運は勇者を助ける。勇気ある行動が幸運を呼ぶ",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "In vino veritas",
     "meaning": "ワインの中に真実がある。酒が入ると本音が出る",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    {"text": "Amor vincit omnia",
     "meaning": "愛はすべてを征服する",
     "country": "古代ローマ（ラテン語）", "flag": "IT"},

    # ─── 古代ギリシャ ──────────────────────────
    {"text": "Γνῶθι σεαυτόν",
     "meaning": "汝自身を知れ。自己認識が知恵の始まり（デルポイの神託）",
     "country": "古代ギリシャ", "flag": "GR"},

    {"text": "Μηδέν ἄγαν",
     "meaning": "何事もほどほどに。過ぎたるは猶及ばざるが如し（デルポイの神託）",
     "country": "古代ギリシャ", "flag": "GR"},

    {"text": "Πᾶν μέτρον ἄριστον",
     "meaning": "すべてにおいて中庸が最善である",
     "country": "古代ギリシャ", "flag": "GR"},

    # ─── 北欧神話（ハーヴァマール）────────────
    {"text": "Deyr fé, deyja frændr, deyr sjálfr it sama;\nen orðstírr deyr aldregi\nhveim er sér góðan getr.",
     "meaning": "牛は死に、親族は死に、あなた自身も死ぬ。しかし決して死なぬものがある――亡き人の功績の名声だ",
     "country": "北欧（ハーヴァマール）", "flag": "IS"},

    # ─── 中国（さらに追加）────────────────────
    {"text": "己所不欲，勿施于人",
     "meaning": "自分がされたくないことは人にするな。思いやりの黄金律（孔子）",
     "country": "中国（孔子）", "flag": "CN"},

    {"text": "民以食为天",
     "meaning": "民は食をもって天とする。食は人の最も根本的な必要",
     "country": "中国", "flag": "CN"},

    {"text": "天生我材必有用",
     "meaning": "天が私を生んだのは必ず用途がある。自分の才能を信じよ（李白）",
     "country": "中国", "flag": "CN"},

    # ─── 韓国（さらに追加）────────────────────
    {"text": "급할수록 돌아가라",
     "meaning": "急ぐときほど回り道をせよ。焦りは禁物",
     "country": "韓国", "flag": "KR"},

    {"text": "지성이면 감천",
     "meaning": "真心があれば天も動く。誠実な努力は必ず報われる",
     "country": "韓国", "flag": "KR"},

    # ─── アラビア（さらに追加）────────────────
    {"text": "الوقت كالسيف إن لم تقطعه قطعك",
     "meaning": "時間は剣のようなもの。使いこなさなければ、時間に使われる",
     "country": "アラビア", "flag": "AE"},

    {"text": "من طلب العلا سهر الليالي",
     "meaning": "高みを目指す者は夜も眠れない。偉業には相応の努力がいる",
     "country": "アラビア", "flag": "AE"},

    # ─── イスラエル（追加）────────────────────
    {"text": "גם זה יעבור",
     "meaning": "これもまた過ぎ去る。困難も喜びも永遠ではない",
     "country": "イスラエル（ヘブライ語）", "flag": "IL"},

    # ─── トルコ（さらに追加）──────────────────
    {"text": "Söz gümüştür, sükût altındır",
     "meaning": "言葉は銀、沈黙は金。語るよりも黙ることが時に価値がある",
     "country": "トルコ", "flag": "TR"},

    # ─── ベトナム（さらに追加）────────────────
    {"text": "Uống nước nhớ nguồn",
     "meaning": "水を飲む時は源を思え。恩恵を受けた人への感謝を忘れるな",
     "country": "ベトナム", "flag": "VN"},

    # ─── ハワイ ────────────────────────────────
    {"text": "I ka ʻōlelo nō ke ola, i ka ʻōlelo nō ka make",
     "meaning": "言葉に命があり、言葉に死がある。言葉の力を大切に",
     "country": "ハワイ（アメリカ）", "flag": "US"},

    {"text": "ʻAʻohe hana nui ke alu ʻia",
     "meaning": "協力すれば大きな仕事も難しくない",
     "country": "ハワイ（アメリカ）", "flag": "US"},

    # ─── サモア ────────────────────────────────
    {"text": "E au le inailau a tamaitai",
     "meaning": "女性の知恵は海のように広く深い",
     "country": "サモア", "flag": "WS"},

    # ─── コスタリカ ────────────────────────────
    {"text": "Pura vida",
     "meaning": "純粋な人生。シンプルに感謝して生きるコスタリカ人の精神",
     "country": "コスタリカ", "flag": "CR"},

    # ─── トリニダード・トバゴ ──────────────────
    {"text": "Every mango have its season",
     "meaning": "すべてのマンゴーには季節がある。万物には適切な時がある",
     "country": "トリニダード・トバゴ", "flag": "TT"},

    # ─── バルバドス ────────────────────────────
    {"text": "De higher the monkey climb,\nde more he expose",
     "meaning": "猿が高く登れば登るほど、より多くさらされる。地位が高いほど批判も増える",
     "country": "バルバドス", "flag": "BB"},

    # ─── ボリビア ──────────────────────────────
    {"text": "Poco a poco se hace lejos",
     "meaning": "少しずつ積み重ねれば遠くへ行ける",
     "country": "ボリビア", "flag": "BO"},

    # ─── ウルグアイ ────────────────────────────
    {"text": "A buen entendedor, pocas palabras bastan",
     "meaning": "聡明な者には少ない言葉で十分。真に理解ある人への短い言葉は雄弁",
     "country": "ウルグアイ", "flag": "UY"},

    # ─── アルバニア ────────────────────────────
    {"text": "Kush nuk punon, nuk ha",
     "meaning": "働かない者は食べてはならない",
     "country": "アルバニア", "flag": "AL"},

    {"text": "Gjuha shpatin të pret",
     "meaning": "舌は剣より鋭く切る。言葉の力を軽んじるな",
     "country": "アルバニア", "flag": "AL"},

    # ─── スロベニア ────────────────────────────
    {"text": "Bolje preprečiti kakor zdraviti",
     "meaning": "治療より予防の方が良い",
     "country": "スロベニア", "flag": "SI"},

    # ─── ベラルーシ ────────────────────────────
    {"text": "Зямля без вады, як сям'я без маці",
     "meaning": "水なき大地は母なき家族のよう。支えあう存在の大切さ",
     "country": "ベラルーシ", "flag": "BY"},

    # ─── ルワンダ ──────────────────────────────
    {"text": "Ubumwe ni nguvu",
     "meaning": "団結は力なり",
     "country": "ルワンダ", "flag": "RW"},

    # ─── コンゴ民主共和国 ──────────────────────
    {"text": "Maboko mibale ebendi moto",
     "meaning": "両手が体を洗う。互いに助け合え",
     "country": "コンゴ民主共和国（リンガラ語）", "flag": "CD"},

    # ─── ソマリア ──────────────────────────────
    {"text": "Aqoon la'aani waa iftiin la'aan",
     "meaning": "知識のない者は光のない者。学びこそが道を照らす",
     "country": "ソマリア", "flag": "SO"},

    # ─── ハウサ語（ナイジェリア・ニジェール）──────
    {"text": "Hankali shi ne mabudin arziki",
     "meaning": "知恵は豊かさの鍵",
     "country": "ハウサ語（ナイジェリア）", "flag": "NG"},

    # ─── イグボ語（ナイジェリア）──────────────
    {"text": "Onye wetara oji wetara ndụ",
     "meaning": "コラナッツを持ってきた者は命をもたらした。分かち合いが生命を与える",
     "country": "イグボ語（ナイジェリア）", "flag": "NG"},

    # ─── パプアニューギニア ────────────────────
    {"text": "Wanbel",
     "meaning": "心を一つにすること。調和と一致の精神（トク・ピシン語）",
     "country": "パプアニューギニア", "flag": "PG"},

    # ─── キルギスタン ──────────────────────────
    {"text": "Жердин кенчи — адамда",
     "meaning": "大地の宝は人にある。人こそが最大の財産",
     "country": "キルギスタン", "flag": "KG"},

    # ─── タジキスタン ──────────────────────────
    {"text": "Дӯст он аст, ки дар рӯзи сахт ёр шавад",
     "meaning": "友とは困難な日に助けてくれる人",
     "country": "タジキスタン", "flag": "TJ"},

    # ─── バングラデシュ ────────────────────────
    {"text": "অভাব অভিযোগ নেই যার, সুখী সে সংসার",
     "meaning": "不満も不平もない家庭こそ幸せな家庭",
     "country": "バングラデシュ", "flag": "BD"},

    # ─── ラオス ────────────────────────────────
    {"text": "ຄວາມອົດທົນຄືຄວາມສຳເລັດ",
     "meaning": "忍耐こそが成功への道",
     "country": "ラオス", "flag": "LA"},

    # ─── ウェールズ（追加）────────────────────
    {"text": "Nid da lle gellir gwell",
     "meaning": "より良くなれる場所に甘んじるな。常に成長を求めよ",
     "country": "ウェールズ", "flag": "GB"},

    # ─── カタルーニャ ──────────────────────────
    {"text": "Qui no s'arrisca, no pisca",
     "meaning": "リスクを取らない者は何も得られない",
     "country": "カタルーニャ（スペイン）", "flag": "ES"},
]

# ==========================================
# 色テーマ
# ==========================================
BG        = "#12131a"   # 最暗部
PANEL     = "#1e2030"   # カード背景
BORDER    = "#2e3050"   # 枠線
TEXT      = "#e8eaf6"   # メインテキスト
DIM       = "#7075a0"   # 薄テキスト
GOLD      = "#ffd166"   # アクセント（金）
TEAL      = "#06d6a0"   # ランダムバッジ
BTN_BG    = "#2e3562"   # ボタン背景
BTN_HV    = "#3d4680"   # ボタンホバー

# ==========================================
# ロジック
# ==========================================
def get_daily_proverb():
    today = datetime.date.today().isoformat()
    idx = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(PROVERBS)
    return PROVERBS[idx], idx

# ==========================================
# アプリ本体
# ==========================================
class ProverbApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_idx = None
        self._setup_window()
        self._build_ui()
        self.show_daily()

    def _setup_window(self):
        self.root.title("世界のことわざ")
        W, H = 720, 460
        self.root.geometry(f"{W}x{H}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw-W)//2}+{(sh-H)//2}")

    def _font(self, size, bold=False):
        weight = "bold" if bold else "normal"
        for name in ("Yu Gothic UI", "Meiryo UI", "Meiryo", "MS Gothic", "TkDefaultFont"):
            try:
                f = tkinter.font.Font(family=name, size=size, weight=weight)
                if f.actual("family").lower() not in ("", "tkdefaultfont"):
                    return f
            except Exception:
                continue
        return tkinter.font.Font(size=size, weight=weight)

    def _build_ui(self):
        # ── ヘッダー ──────────────────────────
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=28, pady=(22, 0))

        self.badge = tk.Label(
            hdr, text="  今日のことわざ  ",
            bg=GOLD, fg=BG,
            font=self._font(9, bold=True),
            padx=4, pady=3, relief="flat"
        )
        self.badge.pack(side="left")

        self.date_lbl = tk.Label(
            hdr,
            text=datetime.date.today().strftime("%Y年 %m月 %d日"),
            bg=BG, fg=DIM, font=self._font(9)
        )
        self.date_lbl.pack(side="right")

        # ── カード ────────────────────────────
        card = tk.Frame(self.root, bg=PANEL, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="both", expand=True, padx=28, pady=12)

        # 国名
        self.country_lbl = tk.Label(
            card, text="", bg=PANEL, fg=DIM, font=self._font(10)
        )
        self.country_lbl.pack(pady=(18, 4))

        # ことわざ本文
        self.proverb_lbl = tk.Label(
            card, text="", bg=PANEL, fg=GOLD,
            font=self._font(20, bold=True),
            wraplength=640, justify="center"
        )
        self.proverb_lbl.pack(pady=(4, 14), padx=24)

        # 区切り線
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=40)

        # 意味
        self.meaning_lbl = tk.Label(
            card, text="", bg=PANEL, fg=TEXT,
            font=self._font(11),
            wraplength=630, justify="center"
        )
        self.meaning_lbl.pack(pady=(14, 20), padx=24)

        # ── ボタン行 ──────────────────────────
        btn_row = tk.Frame(self.root, bg=BG)
        btn_row.pack(fill="x", padx=28, pady=(0, 18))

        self._btn(btn_row, "今日のことわざ", self.show_daily).pack(side="left", padx=(0, 8))
        self._btn(btn_row, "ランダム", self.show_random).pack(side="left", padx=(0, 8))

        self.counter_lbl = tk.Label(
            btn_row, text="", bg=BG, fg=DIM, font=self._font(9)
        )
        self.counter_lbl.pack(side="left", padx=8)

        self._btn(btn_row, "閉じる", self.root.quit, danger=True).pack(side="right")

    def _btn(self, parent, text, cmd, danger=False):
        bg = "#3d2060" if danger else BTN_BG
        return tk.Button(
            parent, text=text, command=cmd,
            bg=bg, fg=TEXT, font=self._font(10),
            relief="flat", bd=0, padx=14, pady=7,
            cursor="hand2",
            activebackground=BTN_HV, activeforeground=TEXT
        )

    def _update(self, proverb, idx, daily=False):
        self.current_idx = idx
        self.country_lbl.config(text=f"[ {proverb['country']} ]")
        self.proverb_lbl.config(text=proverb["text"])
        self.meaning_lbl.config(text=proverb["meaning"])
        self.counter_lbl.config(text=f"{idx + 1} / {len(PROVERBS)}")
        if daily:
            self.badge.config(text="  今日のことわざ  ", bg=GOLD, fg=BG)
        else:
            self.badge.config(text="  ランダム  ", bg=TEAL, fg=BG)

    def show_daily(self):
        p, idx = get_daily_proverb()
        self._update(p, idx, daily=True)

    def show_random(self):
        idx = random.randint(0, len(PROVERBS) - 1)
        while idx == self.current_idx and len(PROVERBS) > 1:
            idx = random.randint(0, len(PROVERBS) - 1)
        self._update(PROVERBS[idx], idx, daily=False)

    def run(self):
        self.root.mainloop()


# ==========================================
# エントリーポイント
# ==========================================
if __name__ == "__main__":
    app = ProverbApp()
    app.run()
