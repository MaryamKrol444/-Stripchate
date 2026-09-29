#!/usr/bin/env python3
"""
Stripchate — static SEO site generator.

Generates the full static site (home page + one page per StripChat typo,
CSS, sitemap, robots, 404, favicon) at the repository root.
Run:  python3 tools/build_site.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- constants
BASE = "https://maryamkrol444.github.io/Stripchate/"
GSC = "Xuf94fNm4YX5BqNwEQruet7zaJzvWqv65AoTLLchIj8"
TODAY = "2026-09-29"

CTA_URL = "https://striptokens.live/stripchat-com/"
CTA_SHORT = "striptokens.live/stripchat-com"

VID_ID = "y9LX8PkDGO4"
VID_EMBED = f"https://www.youtube-nocookie.com/embed/{VID_ID}"
VID_WATCH = f"https://youtu.be/{VID_ID}"
VID_TITLE = "Stripchate vs Stripchat com \U0001f50d Avoid Phishing! Get Cheap Tokens at \U0001f48e StripTokens.live \U0001f48e"
VID_THUMB = f"https://i.ytimg.com/vi/{VID_ID}/hqdefault.jpg"
VID_DURATION = "PT1M31S"

FAVICON = "favicon.svg"

# ---------------------------------------------------------------- typo data
# Each entry targets ONE misspelling with unique, human-written copy.
TYPOS = [
    {
        "slug": "strip-chat-com",
        "kw": "strip chat com",
        "h1": "You typed \u201cstrip chat com\u201d \u2014 did you mean stripchat.com?",
        "title": "strip chat com \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstrip chat com\u201d doesn\u2019t work \u2014 web addresses can\u2019t contain spaces. Here\u2019s why people type it, why the real address is stripchat.com, and how to reach the right site safely.",
        "note": "spaces between the words",
        "why": [
            "This is the \u201cspoken\u201d version of the address. StripChat is two words \u2014 strip and chat \u2014 so people type it the way they say it, as three separate pieces: strip chat com. A domain name, however, cannot contain spaces. The moment you press the space bar, your browser can no longer treat the input as an address; it quietly turns it into a search query instead. That is why you land on search results or \u201cdid you mean?\u201d screens rather than on the site.",
            "The fix is mechanical: remove both spaces, keep the letters in the same order, and you have the real domain \u2014 stripchat.com. This typo is also the least dangerous one on the list, because a spaced string can never be a website, so nothing malicious can answer it. The risk starts only when the typo is itself a real, registered domain.",
        ],
        "faq": [
            ("Why doesn\u2019t \u201cstrip chat com\u201d open the site?",
             "Because it contains spaces, and spaces are not valid in a web address. Your browser treats the string as a search query. Type stripchat.com without any spaces and the site opens."),
            ("Does \u201cwww strip chat\u201d work?",
             "No \u2014 the spaces break it. Without spaces, both stripchat.com and www.stripchat.com take you to the same site."),
            ("Is there a real website called \u201cstrip chat com\u201d?",
             "Not as an address \u2014 that string cannot be a domain. If a link labelled \u201cstrip chat com\u201d loads a page, check the address bar: the only correct domain is stripchat.com."),
        ],
    },
    {
        "slug": "www-strip-chat",
        "kw": "www strip chat",
        "h1": "You typed \u201cwww strip chat\u201d \u2014 did you mean stripchat.com?",
        "title": "www strip chat \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "You typed \u201cwww strip chat\u201d. The real address has no spaces: stripchat.com. Learn why the old www habit causes errors and how to reach StripChat safely.",
        "note": "www. prefix typed as words",
        "why": [
            "Two habits collide here: the old \u201cwww.\u201d prefix from the early web, and typing the name as separate words. Neither part works as an address. \u201cwww\u201d is only meaningful as a subdomain (www.stripchat.com), and spaces break domain syntax entirely \u2014 so the browser again falls back to running a search instead of navigating.",
            "You don\u2019t need \u201cwww\u201d at all anymore. Type stripchat.com exactly and you are there; if you prefer the prefix, www.stripchat.com without spaces resolves to the same site. Bookmark the address once and the habit problem disappears completely.",
        ],
        "faq": [
            ("Do I need \u201cwww\u201d to visit StripChat?",
             "No. Modern browsers fill in the rest when you type stripchat.com. \u201cwww.stripchat.com\u201d also works if you prefer it \u2014 the key is: no spaces."),
            ("Why does \u201cwww strip chat\u201d lead to a search page?",
             "The spaces make the string invalid as a web address, so the browser searches instead. Type the full domain without spaces."),
            ("Is www.stripchat.com a different site from stripchat.com?",
             "No. It is the same website reached through a conventional subdomain."),
        ],
    },
    {
        "slug": "stripchate",
        "kw": "stripchate",
        "h1": "You typed \u201cstripchate\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchate \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "You typed \u201cstripchate\u201d \u2014 that\u2019s StripChat with an extra \u2018e\u2019. The correct address is stripchat.com. See why the typo happens and how to reach the real site.",
        "note": "extra \u201ce\u201d at the end",
        "why": [
            "An extra \u201ce\u201d at the end is the single most common misspelling of the name \u2014 it is even the name of this site. Two forces create it. First, \u201ce\u201d sits next to the space bar on many layouts, so a mistimed keystroke appends it. Second, a trailing vowel makes the word feel \u201ccomplete\u201d to the ear. Because the result looks so close to the real name, \u201cstripchate\u201d is exactly the kind of string someone registers as a domain.",
            "The check is always the address bar. If the domain reads stripchate.com, stripchate.net or anything else, you are not on StripChat. The real address is stripchat.com \u2014 nine letters before the dot and no letter after the \u201ct\u201d. Never enter your password on a \u201cstripchate\u201d domain.",
        ],
        "faq": [
            ("Is stripchate the same as StripChat?",
             "No. StripChat is spelled s-t-r-i-p-c-h-a-t, and its address is stripchat.com. \u201cStripchate\u201d adds an extra \u201ce\u201d at the end \u2014 which is exactly why this page exists."),
            ("Is stripchate.com safe to use?",
             "It is not the official site. Whether it is harmless or harmful, it is not StripChat \u2014 do not enter your login details there. Use stripchat.com."),
            ("What is this website (Stripchate)?",
             "Stripchate is an independent spelling helper that catches common typos of the StripChat name and points you to the correct address, stripchat.com."),
        ],
    },
    {
        "slug": "stripchata",
        "kw": "stripchata",
        "h1": "You typed \u201cstripchata\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchata \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "You typed \u201cstripchata\u201d \u2014 an extra \u2018a\u2019 that is common in Slavic speech. The correct address is stripchat.com. Why the typo happens and how to fix it, explained.",
        "note": "extra \u201ca\u201d at the end",
        "why": [
            "The trailing \u201ca\u201d is the signature typo for users of Polish, Russian, Czech, Ukrainian and other Slavic languages. In everyday speech the brand name naturally takes a grammatical ending \u2014 \u201cdo Stripchata\u201d, \u201cna Stripchacie\u201d \u2014 and that spoken form ends up in the browser. It is a linguistic slip rather than a keyboard one, which is why the same person repeats it over and over.",
            "Spoken forms do not travel to the address bar. The platform\u2019s name is StripChat and its domain is stripchat.com \u2014 no case endings, no extra vowels. If a \u201cstripchata\u201d domain ever loads for you, treat it as an impostor until you have confirmed otherwise, and close it before typing anything personal.",
        ],
        "faq": [
            ("Is \u201cstripchata\u201d a real website?",
             "It is not the platform\u2019s address. The correct domain is stripchat.com. \u201cStripchata\u201d is the spoken, grammatically-ended form of the name that is common in Slavic languages."),
            ("Why does my phone suggest \u201cstripchata\u201d?",
             "Predictive text learns from your typing and from the languages you use. Replace the suggestion by typing stripchat.com in full, then bookmark it."),
            ("Can I log in at stripchata.com?",
             "No \u2014 credentials should only ever be entered at stripchat.com. Any other domain asking for your password is not the real site."),
        ],
    },
    {
        "slug": "stripchat-cim",
        "kw": "stripchat cim",
        "h1": "You typed \u201cstripchat cim\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchat cim \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstripchat cim\u201d is a one-key typo: \u2018i\u2019 sits next to \u2018o\u2019 on the keyboard. The correct address is stripchat.com. Why it happens and how to avoid fake \u201ccim\u201d domains.",
        "note": "\u201co\u201d typed as \u201ci\u201d",
        "why": [
            "In \u201ccim\u201d the letter \u201co\u201d became \u201ci\u201d. On a QWERTY keyboard the two keys are neighbours on the top row, so a half-key drift in the final part of the address produces it. The space before it makes things worse: browsers treat \u201cstripchat cim\u201d as two words and run a search. But if the space is accidentally missed (\u201cstripchatcim.com\u201d), you are at the mercy of whoever registered that domain.",
            "The real extension is .com \u2014 c, o, m \u2014 and only the letter o. Because \u201ccim\u201d is a predictable one-key error on a high-traffic brand, typo domains like it are routinely parked with ads or, worse, lookalike login screens. Never enter a password or a card number on a page whose address bar does not read exactly stripchat.com.",
        ],
        "faq": [
            ("What is the difference between .com and .cim?",
             ".com is a real top-level domain; there is no .cim. \u201cCim\u201d is what \u201c.com\u201d becomes when the \u201co\u201d is typed as \u201ci\u201d \u2014 two neighbouring keys."),
            ("Is \u201cstripchat cim\u201d a valid address?",
             "No. The correct address is stripchat.com \u2014 one word, a dot, then c-o-m."),
            ("What should I do if a \u201ccim\u201d site asks for my password?",
             "Close the tab immediately. The genuine site only asks for credentials at stripchat.com."),
        ],
    },
    {
        "slug": "stripchat-clm",
        "kw": "stripchat clm",
        "h1": "You typed \u201cstripchat clm\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchat clm \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstripchat clm\u201d swaps \u2018o\u2019 for \u2018l\u2019, two nearby keys apart. The correct address is stripchat.com. Learn why this typo happens and how to stay safe online.",
        "note": "\u201co\u201d typed as \u201cl\u201d",
        "why": [
            "\u201cclm\u201d is \u201c.com\u201d with the \u201co\u201d replaced by \u201cl\u201d. On a full-size keyboard the keys are not directly adjacent, but on small phone keyboards \u201cl\u201d sits just below and to the right of \u201co\u201d \u2014 a common thumb slip, especially on the tiny on-screen keyboards used in a hurry.",
            "There is no \u201c.clm\u201d top-level domain, so \u201cstripchat clm\u201d can never be the real site. The correct address is stripchat.com. If a page that asks for your login ever loads from any other domain, close the tab \u2014 the genuine site only asks for credentials at stripchat.com.",
        ],
        "faq": [
            ("Is \u201cclm\u201d a typo of \u201ccom\u201d?",
             "Yes \u2014 the \u201co\u201d has been replaced by \u201cl\u201d. The correct extension is .com."),
            ("Does a .clm domain exist?",
             "There is no .clm top-level domain, so any address ending in \u201clm\u201d in this context is not the real site."),
            ("How do I reach StripChat correctly?",
             "Type stripchat.com in the address bar, confirm the padlock and the exact domain, and bookmark it for next time."),
        ],
    },
    {
        "slug": "stripchat-c0m",
        "kw": "stripchat c0m",
        "h1": "You typed \u201cstripchat c0m\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchat c0m \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstripchat c0m\u201d uses the number zero instead of the letter o. There is no .c0m \u2014 the real address is stripchat.com. Why the mix-up happens, explained.",
        "note": "\u201co\u201d typed as \u201c0\u201d (zero)",
        "why": [
            "Here the letter \u201co\u201d was typed as the number zero (0). It happens on multi-layer phone keyboards where you briefly hold a modifier key, and it happens out of habit for anyone who uses leetspeak online. Domain names can legally contain digits, which makes \u201cc0m\u201d especially sneaky: it looks right at a glance, but there is no such thing as a .c0m \u2014 only .com, with the round letter.",
            "The rule: the extension is three letters, c-o-m. If the address bar shows a zero anywhere in the domain, you are on the wrong site \u2014 possibly one registered specifically to catch people who make this mistake. Verify the exact domain before you type anything sensitive.",
        ],
        "faq": [
            ("What is the difference between \u201co\u201d and \u201c0\u201d in the domain?",
             "The correct character is the round letter o, as in .com. A zero (0) creates an invalid or fake domain \u2014 the two look almost identical, which is the point of the trap."),
            ("Is stripchat.c0m safe?",
             "No. It is not the official address. Confirm that the domain reads exactly stripchat.com before entering anything personal."),
            ("How do I type the correct address on a phone keyboard?",
             "Stay on the letters layer for the whole address \u2014 stripchat.com \u2014 without switching to numbers. Bookmark it once to skip typing altogether."),
        ],
    },
    {
        "slug": "stripchat-con",
        "kw": "stripchat con",
        "h1": "You typed \u201cstripchat con\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchat con \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstripchat con\u201d is one keystroke away from the truth: \u2018n\u2019 sits next to \u2018m\u2019. The correct address is stripchat.com. Why the typo happens and how to fix it.",
        "note": "\u201cm\u201d typed as \u201cn\u201d",
        "why": [
            "\u201ccon\u201d is \u201c.com\u201d with the final \u201cm\u201d struck as \u201cn\u201d \u2014 the two keys sit side by side on the bottom row, and \u201cn\u201d is where your finger drifts when you reach for enter a fraction early. It is one of the fastest typos to make, and one of the most common in searches for this brand.",
            "There is no \u201c.con\u201d for this purpose; the correct address is stripchat.com. Change that last letter and you are done. And because predictable misspellings get registered by opportunists, a \u201ccon\u201d address that ever loads a login form is a red flag, not a coincidence \u2014 close it.",
        ],
        "faq": [
            ("Is \u201cstripchat con\u201d a typo of \u201cstripchat com\u201d?",
             "Yes \u2014 the final \u201cm\u201d was typed as \u201cn\u201d, the key directly to its left."),
            ("Can .con be a real extension here?",
             "No. The correct address is stripchat.com, and nothing else."),
            ("Why do I keep making this one-key mistake?",
             "Because \u201cm\u201d and \u201cn\u201d are neighbours and the slip happens at the moment you are about to press enter. A bookmark removes the typing entirely."),
        ],
    },
    {
        "slug": "stripchat-fom",
        "kw": "stripchat fom",
        "h1": "You typed \u201cstripchat fom\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchat fom \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "\u201cstripchat fom\u201d types \u2018f\u2019 instead of \u2018c\u2019 \u2014 f sits directly above c on most keyboards. The correct address is stripchat.com. How to avoid this typo, explained.",
        "note": "\u201cc\u201d typed as \u201cf\u201d",
        "why": [
            "\u201cfom\u201d is \u201c.com\u201d with the \u201cc\u201d replaced by \u201cf\u201d \u2014 and that is no random choice: on QWERTY keyboards, f sits directly above c, in the same column. A finger that lands one row too high types \u201cfom\u201d instead of \u201ccom\u201d. One-finger typers hit it disproportionately often.",
            "The fix is either to slow down one keystroke or to stop typing the address at all: bookmark stripchat.com once and let the browser do the remembering. The correct extension is .com with the letter c \u2014 and any other domain is not StripChat.",
        ],
        "faq": [
            ("Why do I keep typing \u201cfom\u201d instead of \u201ccom\u201d?",
             "Because on QWERTY keyboards the \u201cf\u201d key sits directly above \u201cc\u201d. A finger that lands one row high produces \u201cfom\u201d."),
            ("Is .fom a real domain extension?",
             "No \u2014 the extension is .com. A \u201cfom\u201d address that loads a page is a different website, not StripChat."),
            ("How can I stop making this error?",
             "Bookmark stripchat.com so you do not type the address at all, or simply slow down on the first letter of the extension."),
        ],
    },
    {
        "slug": "stripchay",
        "kw": "stripchay",
        "h1": "You typed \u201cstripchay\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchay \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "You typed \u201cstripchay\u201d \u2014 \u2018y\u2019 sits next to \u2018t\u2019. The real name ends in -t: StripChat. The correct address is stripchat.com. Why the slip happens, explained.",
        "note": "\u201ct\u201d typed as \u201cy\u201d",
        "why": [
            "The last \u201ct\u201d of \u201cstripchat\u201d became \u201cy\u201d \u2014 the two keys are neighbours on the top row, so the final keystroke drifts one to the right and the name collapses into \u201cstripchay\u201d. Because the error sits at the very end of the word, it is easy to miss when you scan the address bar quickly.",
            "The name ends in \u201ct\u201d: s-t-r-i-p-c-h-a-t. The full correct address is stripchat.com. A \u201cstripchay\u201d domain is not the platform, and pages served from it should be treated as untrusted \u2014 close them and type the correct address yourself.",
        ],
        "faq": [
            ("Is \u201cstripchay\u201d the same as StripChat?",
             "No \u2014 the name ends in \u201ct\u201d, not \u201cy\u201d. The correct address is stripchat.com."),
            ("Why does my browser show search results for \u201cstripchay\u201d?",
             "Because it is not a valid domain; the browser falls back to a search. Correct the final letter and type stripchat.com."),
            ("Is a \u201cstripchay\u201d website dangerous?",
             "It is not the official site, so treat it as untrusted \u2014 especially if it asks for a password or payment details."),
        ],
    },
    {
        "slug": "stripchst",
        "kw": "stripchst",
        "h1": "You typed \u201cstripchst\u201d \u2014 did you mean stripchat.com?",
        "title": "stripchst \u2014 Did You Mean stripchat.com? | Stripchate",
        "desc": "You typed \u201cstripchst\u201d \u2014 the \u2018a\u2019 in \u2018chat\u2019 was dropped. The correct spelling is stripchat, and the address is stripchat.com. Why it happens and how to fix it.",
        "note": "\u201ca\u201d dropped from \u201cchat\u201d",
        "why": [
            "\u201cstripchst\u201d is missing the \u201ca\u201d from \u201cchat\u201d \u2014 the word shrank from eight letters to seven while being typed. Dropped middle letters are typical of fast typing and of accepting a keyboard suggestion before checking it. The result looks almost right, which is exactly what makes it worth a careful look at the address bar.",
            "Every letter matters: s-t-r-i-p-c-h-a-t. Restore the missing \u201ca\u201d, add .com, and you have the real domain \u2014 stripchat.com. If the mistyped address ever resolves to a page, it belongs to someone else; never share a password there.",
        ],
        "faq": [
            ("Is \u201cstripchst\u201d a valid spelling?",
             "No \u2014 it is missing the \u201ca\u201d in \u201cchat\u201d. The correct spelling is s-t-r-i-p-c-h-a-t."),
            ("What is the full correct address?",
             "stripchat.com \u2014 every letter of the name, then a dot, then c-o-m."),
            ("How do I fix the mistake quickly?",
             "Add the missing \u201ca\u201d back (stripch-st \u2192 stripchat) and type stripchat.com. A bookmark makes the next visit a single tap."),
        ],
    },
]

# ---------------------------------------------------------------- helpers
def video_jsonld(abs_url):
    return {
        "@type": "VideoObject",
        "@id": abs_url + "#video",
        "name": VID_TITLE,
        "description": ("Short video guide: why common StripChat typos (stripchate, stripchata, "
                        "strip chat com, www strip chat, stripchat cim, clm, c0m, con, fom, "
                        "stripchay, stripchst) can lead to phishing sites, and what the correct "
                        "address \u2014 stripchat.com \u2014 is."),
        "thumbnailUrl": VID_THUMB,
        "uploadDate": TODAY + "T00:00:00+00:00",
        "duration": VID_DURATION,
        "embedUrl": f"https://www.youtube.com/embed/{VID_ID}",
        "contentUrl": f"https://www.youtube.com/watch?v={VID_ID}",
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "SMCRecordings"},
    }

def org_jsonld(abs_url, extra=None):
    node = {
        "@type": "Organization",
        "@id": abs_url + "#organization",
        "name": "Stripchate",
        "url": BASE,
        "description": "Independent spelling helper for the StripChat name \u2014 explains common typos and points to the correct address, stripchat.com.",
        "sameAs": ["https://striptokens.live"],
    }
    if extra:
        node.update(extra)
    return node

def faq_jsonld(abs_url, faq):
    return {
        "@type": "FAQPage",
        "@id": abs_url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def jsonld(nodes):
    return "<script type=\"application/ld+json\">\n" + json.dumps(nodes, indent=2, ensure_ascii=False) + "\n</script>"

def video_block(iframe_title):
    return f'''  <figure class="hero-video">
    <div class="video-frame">
      <iframe src="{VID_EMBED}" title="{esc(iframe_title)}"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen></iframe>
    </div>
    <figcaption>\U0001f3ac <a href="{VID_WATCH}">{esc(VID_TITLE)} \u2014 watch on YouTube \u2197</a></figcaption>
  </figure>'''

def sticky_cta():
    return f'''  <aside class="sticky-cta" aria-label="Stripchat.com guide and tokens">
    <a href="{CTA_URL}">
      <span class="cta-emoji" aria-hidden="true">\U0001f39f\ufe0f</span>
      <span class="cta-text"><strong>StripChat tokens</strong> + the <strong>stripchat.com</strong> address guide</span>
      <span class="cta-url">{CTA_SHORT} \u2192</span>
    </a>
  </aside>'''

def footer(prefix):
    return f'''  <footer class="site-footer">
    <div class="container">
      <p class="about"><strong>Stripchate</strong> is an independent spelling helper for the StripChat name.
      We are not affiliated with, endorsed by, or connected to StripChat. \u201cStripChat\u201d is a trademark of its respective owner.</p>
      <p class="fineprint">Intended for adults (18+). No explicit content is shown on this site.
      The correct address for the platform is <a href="https://stripchat.com" rel="noopener nofollow">stripchat.com</a>.</p>
      <p class="foot-links">
        <a href="{prefix}">Home</a> \u00b7
        <a href="{prefix}#typo-directory">All typos</a> \u00b7
        <a href="https://stripchat.com" rel="noopener nofollow">stripchat.com (official)</a> \u00b7
        <a href="{CTA_URL}">Stripchat.com guide \u2014 {CTA_SHORT}</a>
      </p>
    </div>
  </footer>'''

def head(prefix, title, desc, abs_url, og_type, jsonld_nodes):
    home = prefix == ""
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{abs_url}">
  <meta name="google-site-verification" content="{GSC}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="theme-color" content="#0e1116">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{abs_url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:image" content="{VID_THUMB}">
  <meta property="og:site_name" content="Stripchate">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="{abs_url}">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{VID_THUMB}">
  <link rel="icon" href="{prefix}{FAVICON}" type="image/svg+xml">
  <link rel="preconnect" href="https://www.youtube-nocookie.com">
  <link rel="preconnect" href="https://i.ytimg.com" crossorigin>
  <link rel="stylesheet" href="{prefix}style.css">
  {jsonld(jsonld_nodes)}
</head>
'''

def header(prefix):
    if prefix == "":
        home = f'''      <a class="brand" href="./">Stripchate<span class="brand-sub">StripChat spelling helper</span></a>
      <nav aria-label="Main navigation">
        <a href="./#typo-directory" class="active">All typos</a>
        <a href="./#safe">Get there safely</a>
        <a href="{CTA_URL}" class="nav-cta">\U0001f39f\ufe0f Tokens &amp; guide</a>
      </nav>'''
    else:
        home = f'''      <a class="brand" href="../">Stripchate<span class="brand-sub">StripChat spelling helper</span></a>
      <nav aria-label="Main navigation">
        <a href="../">Home</a>
        <a href="../#typo-directory">All typos</a>
        <a href="{CTA_URL}" class="nav-cta">\U0001f39f\ufe0f Tokens &amp; guide</a>
      </nav>'''
    return f'''<body>
  <div class="age-banner" role="note">
    <span><strong>18+ notice:</strong> this site is about an adult platform and links to adult content. No explicit content is shown here.</span>
  </div>
  <header class="site-header">
    <div class="container header-inner">
{home}
    </div>
  </header>
  <main class="container" id="main">
'''

def cta_box():
    return f'''  <section class="cta-box" aria-label="Stripchat.com guide and tokens">
    <h2>Where to get StripChat tokens \u2014 safely</h2>
    <p>The official site is free to browse; tokens are bought separately for tipping and private
    sessions. If you want the correct address walked through step by step, a breakdown of which
    misspelled domains are risky, or a comparison of where to buy tokens, the independent guide at
    <strong>striptokens.live</strong> covers all of it in one place.</p>
    <p><a class="btn btn-primary" href="{CTA_URL}">Open the stripchat.com guide at striptokens.live \u2192</a></p>
    <p class="cta-fineprint">Independent guide \u2014 not the official StripChat site. Intended for adults 18+.</p>
  </section>'''

def related_grid(current_slug):
    items = []
    for t in TYPOS:
        if t["slug"] == current_slug:
            continue
        items.append(
            f'      <li><a href="../{t["slug"]}/"><code>{esc(t["kw"])}</code><span>{esc(t["note"])}</span></a></li>'
        )
    return ('  <section aria-label="Other common StripChat misspellings">\n'
            '    <h2>Other common StripChat misspellings</h2>\n'
            '    <ul class="typo-grid">\n' + "\n".join(items) + "\n    </ul>\n  </section>")

def faq_section(faq):
    blocks = []
    for q, a in faq:
        blocks.append(f'''    <details>
      <summary>{esc(q)}</summary>
      <p>{esc(a)}</p>
    </details>''')
    return '  <section class="faq" aria-label="Frequently asked questions">\n    <h2>Frequently asked questions</h2>\n' + "\n".join(blocks) + "\n  </section>"

# ---------------------------------------------------------------- pages
def page_home():
    title = "StripChat Typos & Misspellings: Did You Mean stripchat.com? | Stripchate"
    desc = ("Typed \u201cstripchate\u201d, \u201cstrip chat com\u201d or \u201cstripchat cim\u201d? This guide covers every common "
            "StripChat misspelling, the correct address \u2014 stripchat.com \u2014 and how to avoid fake typo domains.")
    abs_url = BASE
    nodes = [
        {"@type": "WebSite", "@id": abs_url + "#website", "url": abs_url,
         "name": "Stripchate \u2014 StripChat Spelling Helper", "inLanguage": "en-US"},
        org_jsonld(abs_url),
        {"@type": "BreadcrumbList", "@id": abs_url + "#breadcrumb",
         "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url}]},
        video_jsonld(abs_url),
        faq_jsonld(abs_url, HOME_FAQ),
    ]
    html = head("", title, desc, abs_url, "website", nodes)
    html += header("")
    html += "\n" + video_block("StripChat typos and the correct address \u2014 video guide") + "\n"
    html += '''
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol><li aria-current="page">Home \u2014 StripChat typos &amp; misspellings</li></ol>
  </nav>
  <h1>Did you mean stripchat.com? The complete StripChat typo guide.</h1>
  <p class="lede">If you ended up here, you most likely typed one of the many misspellings of StripChat\u2019s
  address \u2014 stripchate, strip chat com, stripchat cim, stripchat c0m, or one of the others in the table
  below. That is exactly what this site is for: it lists the typos people actually make, explains why each one
  happens, and shows you the correct address \u2014 <strong>stripchat.com</strong> \u2014 plus the safest way to reach it.</p>

  <div class="answer-box" role="note">
    <p><strong>The correct address is <a href="https://stripchat.com" rel="noopener nofollow">stripchat.com</a></strong>
    \u2014 spelled <span class="spell">s\u00b7t\u00b7r\u00b7i\u00b7p\u00b7c\u00b7h\u00b7a\u00b7t</span>, then a dot,
    then <span class="spell">c\u00b7o\u00b7m</span>. One word. No hyphen. No spaces. No zero.</p>
    <p><a class="btn btn-primary" href="''' + CTA_URL + '''">StripChat tokens &amp; the address guide \u2014 striptokens.live \u2192</a></p>
    <p class="cta-fineprint">Independent guide: correct address, common misspellings &amp; safe login. Adults 18+.</p>
  </div>

  <section id="typo-directory" aria-label="Directory of common StripChat typos">
    <h2>Every common StripChat typo, explained</h2>
    <p>Each row below is a real, frequently-searched misspelling. Open the full page for the exact
    explanation of why that particular mistake happens and how to fix it.</p>
    <div class="table-wrap">
    <table>
      <thead>
        <tr><th scope="col">What people type</th><th scope="col">What happened</th><th scope="col">The real address</th><th scope="col">Explain</th></tr>
      </thead>
      <tbody>
'''
    for t in TYPOS:
        html += (f'        <tr><th scope="row"><a href="{t["slug"]}/"><code>{esc(t["kw"])}</code></a></th>'
                 f'<td>{esc(t["note"])}</td>'
                 f'<td><code>stripchat.com</code></td>'
                 f'<td><a class="row-link" href="{t["slug"]}/">Read \u2192</a></td></tr>\n')
    html += '''      </tbody>
    </table>
    </div>
  </section>

  <section aria-label="Why stripchat.com gets mistyped">
    <h2>Why stripchat.com gets mistyped so often</h2>
    <p>The name is short, two-word, and phonetically easy to bend \u2014 which is precisely why it produces a
    large, predictable set of misspellings. The typos on this site fall into five families:</p>
    <ol>
      <li><strong>Spoken-form typos</strong> \u2014 <code>strip chat com</code> and <code>www strip chat</code>: the name
      is typed the way it is said, with spaces and the old \u201cwww\u201d prefix.</li>
      <li><strong>Trailing-vowel typos</strong> \u2014 <code>stripchate</code> and <code>stripchata</code>: an extra vowel at the
      end, from a mistimed \u201ce\u201d next to the space bar or from grammatical endings in Slavic speech.</li>
      <li><strong>One-key extension typos</strong> \u2014 <code>stripchat cim</code>, <code>stripchat con</code>,
      <code>stripchat fom</code>: a single adjacent-key slip inside \u201c.com\u201d.</li>
      <li><strong>Substitution typos</strong> \u2014 <code>stripchat clm</code> (o \u2192 l) and <code>stripchat c0m</code>
      (o \u2192 zero).</li>
      <li><strong>Dropped and shifted letters</strong> \u2014 <code>stripchay</code> (t \u2192 y) and <code>stripchst</code>
      (missing \u201ca\u201d).</li>
    </ol>
  </section>

  <section id="danger" aria-label="Are typo domains dangerous">
    <h2>Are typo domains dangerous?</h2>
    <p>Here is the part that matters for your safety. The first two families above are harmless: a spaced
    address cannot be a website, so nothing can answer it. The extension and substitution families are
    different \u2014 they are so predictable that someone usually registers the resulting domains on purpose.
    What sits on those domains ranges from parked ad pages to convincing copies of the login screen built
    to harvest credentials.</p>
    <p>The one rule that covers every case: <strong>enter your password only where the address bar reads
    exactly stripchat.com</strong> \u2014 nothing appended, nothing prepended, with a padlock. Read the domain
    right-to-left from the first slash; that is the real domain, and everything else on the page can be faked.</p>
  </section>

  <section id="safe" aria-label="How to reach StripChat safely">
    <h2>How to reach StripChat without typos</h2>
    <ol>
      <li><strong>Type the full address yourself:</strong> stripchat.com. For this one, don\u2019t trust forwarded
      links or unknown search ads.</li>
      <li><strong>Verify before you log in:</strong> https + padlock, domain exactly stripchat.com. Read
      right-to-left from the first slash.</li>
      <li><strong>Bookmark it.</strong> One tap beats eleven possible typos.</li>
      <li><strong>If a typo page ever loads and shows a login form:</strong> close it, and don\u2019t download
      anything from it.</li>
    </ol>
  </section>
'''
    html += cta_box()
    html += faq_section(HOME_FAQ)
    html += footer("")
    html += "\n" + sticky_cta() + "\n</main>\n" + footer_close() + "\n</body>\n</html>\n"
    return title, desc, abs_url, html

def footer_close():
    return ""  # footer rendered inside main? no — render before sticky cta; see builder

def page_sub(t, others):
    title = t["title"]
    desc = t["desc"]
    abs_url = BASE + t["slug"] + "/"
    nodes = [
        {"@type": "Article",
         "headline": t["h1"].split("?")[0].strip() + " \u2014 did you mean stripchat.com?",
         "description": desc,
         "mainEntityOfPage": {"@type": "WebPage", "@id": abs_url},
         "datePublished": TODAY,
         "dateModified": TODAY,
         "inLanguage": "en",
         "author": {"@type": "Organization", "name": "Stripchate"},
         "publisher": {"@type": "Organization", "name": "Stripchate", "url": BASE}},
        {"@type": "BreadcrumbList", "@id": abs_url + "#breadcrumb",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
             {"@type": "ListItem", "position": 2, "name": t["kw"]},
         ]},
        video_jsonld(abs_url),
        faq_jsonld(abs_url, t["faq"]),
    ]
    html = head("../", title, desc, abs_url, "article", nodes)
    html += header("../")
    html += "\n" + video_block(t["kw"] + " \u2014 did you mean stripchat.com? (video guide)") + "\n"
    html += f'''
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol>
      <li><a href="../">Home</a></li>
      <li aria-current="page">{esc(t["kw"])}</li>
    </ol>
  </nav>
  <h1>{esc(t["h1"])}</h1>
  <p class="lede">You are on the right page. Below is exactly what \u201c{esc(t["kw"])}\u201d is, why it happens,
  and \u2014 most importantly \u2014 where the real site actually lives.</p>

  <div class="answer-box" role="note">
    <p><strong>The correct address is <a href="https://stripchat.com" rel="noopener nofollow">stripchat.com</a></strong>
    \u2014 spelled <span class="spell">s\u00b7t\u00b7r\u00b7i\u00b7p\u00b7c\u00b7h\u00b7a\u00b7t</span>, then a dot,
    then <span class="spell">c\u00b7o\u00b7m</span>.</p>
    <p><a class="btn btn-primary" href="''' + CTA_URL + '''">StripChat tokens &amp; the address guide \u2014 striptokens.live \u2192</a></p>
    <p class="cta-fineprint">Independent guide: correct address, common misspellings &amp; safe login. Adults 18+.</p>
  </div>

  <section aria-label="Why this typo happens">
    <h2>Why \u201c''' + esc(t["kw"]) + '''\u201d happens</h2>
'''
    for p in t["why"]:
        html += "    <p>" + esc(p) + "</p>\n"
    html += f'''  </section>

  <section id="safe" aria-label="How to reach StripChat safely">
    <h2>How to get to StripChat safely</h2>
    <ol>
      <li><strong>Type the correct address yourself:</strong> stripchat.com \u2014 not \u201c{esc(t["kw"])}\u201d.
      Don\u2019t trust forwarded links or unknown search ads for this one.</li>
      <li><strong>Check the address bar:</strong> https + padlock, and the domain must read exactly
      stripchat.com. Read right-to-left from the first slash \u2014 that is the real domain.</li>
      <li><strong>Bookmark it</strong> (the star icon) so your next visit is one tap, not one typo.</li>
      <li><strong>Never enter your password or payment details</strong> on any other domain \u2014 not on a
      \u201cguide\u201d, not on a link someone sent you. The genuine site asks for credentials only at stripchat.com.</li>
    </ol>
  </section>
'''
    html += cta_box()
    html += related_grid(t["slug"])
    html += faq_section(t["faq"])
    html += footer("../")
    html += "\n" + sticky_cta() + "\n</main>\n</body>\n</html>\n"
    return title, desc, abs_url, html

def head404(title, desc, abs_url, jsonld_nodes):
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{abs_url}">
  <meta name="google-site-verification" content="{GSC}" />
  <meta name="theme-color" content="#0e1116">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{abs_url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <link rel="icon" href="{BASE}{FAVICON}" type="image/svg+xml">
  <link rel="stylesheet" href="{BASE}style.css">
  {jsonld(jsonld_nodes)}
</head>
<body>
  <div class="age-banner" role="note">
    <span><strong>18+ notice:</strong> this site is about an adult platform and links to adult content. No explicit content is shown here.</span>
  </div>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{BASE}">Stripchate<span class="brand-sub">StripChat spelling helper</span></a>
      <nav aria-label="Main navigation">
        <a href="{BASE}">Home</a>
        <a href="{BASE}#typo-directory">All typos</a>
        <a href="{CTA_URL}" class="nav-cta">\U0001f39f\ufe0f Tokens &amp; guide</a>
      </nav>
    </div>
  </header>
  <main class="container" id="main">
'''

def page_404():
    title = "Page not found | Stripchate"
    desc = "This page does not exist. Head back to the StripChat typo guide and find the correct address: stripchat.com."
    abs_url = BASE
    nodes = [org_jsonld(abs_url),
             {"@type": "BreadcrumbList",
              "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url}]}]
    html = head404(title, desc, abs_url, nodes)
    html += f'''
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol><li><a href="{BASE}">Home</a></li><li aria-current="page">Page not found</li></ol>
  </nav>
  <h1>404 \u2014 this page does not exist</h1>
  <p class="lede">The address you followed is not on this site \u2014 ironically, that is exactly the kind of
  \u201cmistyped address\u201d problem this site is about. The one address that is never mistyped here:
  <strong>stripchat.com</strong>.</p>
  <div class="answer-box" role="note">
    <p><a class="btn btn-primary" href="{BASE}">Back to the typo guide \u2190</a>
    <a class="btn" href="{CTA_URL}">StripChat tokens &amp; guide \u2014 striptokens.live \u2192</a></p>
  </div>
  <section aria-label="Quick links">
    <h2>Looking for a specific typo?</h2>
    <ul class="typo-grid">
'''
    for t in TYPOS:
        html += f'      <li><a href="{BASE}{t["slug"]}/"><code>{esc(t["kw"])}</code></a></li>\n'
    html += '''    </ul>
  </section>
'''
    html += footer(BASE)
    html += "\n" + sticky_cta() + "\n</main>\n</body>\n</html>\n"
    return html

# ---------------------------------------------------------------- home FAQ
HOME_FAQ = [
    ("What is the correct website address for StripChat?",
     "The correct address is stripchat.com \u2014 one word before the dot, no hyphen, no space, no extra letters, and an extension of the letters c-o-m, not a zero or a nearby key."),
    ("Is stripchate.com the same as stripchat.com?",
     "No. \u201cStripchate\u201d is a common misspelling (an extra \u2018e\u2019), and any domain containing it is a different website. Only stripchat.com is the real platform \u2014 always confirm the address bar before logging in."),
    ("Why does typing \u201cstrip chat com\u201d show search results instead of the site?",
     "Domain names cannot contain spaces. When you type the name as separate words, your browser cannot treat it as an address, so it runs a search instead. Close the spaces and type stripchat.com."),
    ("Are typo domains like stripchat.con or stripchat.cim dangerous?",
     "They can be. Misspellings of popular sites are predictable, so they get registered by third parties \u2014 sometimes with ad pages, sometimes with lookalike login screens meant to steal credentials. Never enter a password anywhere except stripchat.com."),
    ("Where can I buy StripChat tokens?",
     "Tokens are purchased on the official StripChat site. If you want a comparison of options or a full walkthrough of the address and a safe login, the independent guide at striptokens.live/stripchat-com explains how it works."),
]

# ---------------------------------------------------------------- build
def build():
    # clean generated dirs
    for t in TYPOS:
        d = os.path.join(ROOT, t["slug"])
        if os.path.isdir(d):
            shutil.rmtree(d)
    for f in ("index.html", "404.html", "style.css", "sitemap.xml", "robots.txt",
              FAVICON, ".nojekyll"):
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            os.remove(p)

    pages = []  # (abs_url, title)

    _, _, abs_url, html = page_home()
    write("index.html", html)
    pages.append((abs_url, "home"))

    for t in TYPOS:
        _, _, abs_url, html = page_sub(t, TYPOS)
        write(t["slug"] + "/index.html", html)
        pages.append((abs_url, t["kw"]))

    write("404.html", page_404())
    write("style.css", CSS)
    write(FAVICON, FAVICON_SVG)
    write(".nojekyll", "")

    # robots
    write("robots.txt",
          "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n")

    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for abs_url, _ in pages:
        sm.append(f"  <url><loc>{abs_url}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")

    print(f"Built {len(pages)} indexable pages.")

def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)

# ---------------------------------------------------------------- css
FAVICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0e1116"/>
  <path d="M42 22c-2.5-3.5-7-5.5-12-5.5-7 0-12 3.5-12 8.5S23 30 30 32s12 4 12 9-5 8.5-12 8.5c-5 0-9.5-2-12-5.5"
        fill="none" stroke="#ff4d6d" stroke-width="5.5" stroke-linecap="round"/>
</svg>
'''

CSS = '''/* Stripchate — dark, fast, mobile-first. No JS required. */
:root{
  --bg:#0e1116; --bg-2:#151a22; --bg-3:#1b2230;
  --text:#e8ecf1; --muted:#9aa7b8; --line:#2a3342;
  --accent:#ff4d6d; --accent-2:#ff8fa3; --blue:#4da3ff;
  --ok:#3ddc97; --radius:14px;
  --sticky-h:64px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--text);
  font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  padding-bottom:calc(var(--sticky-h) + 24px);
  -webkit-font-smoothing:antialiased;
}
img,iframe{max-width:100%}
a{color:var(--blue); text-decoration-thickness:1px; text-underline-offset:2px}
a:hover{color:#7cbcff}
code{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  background:var(--bg-3); border:1px solid var(--line);
  border-radius:6px; padding:.1em .4em; font-size:.92em; color:#ffd98a;
  word-break:break-word;
}
.container{max-width:920px; margin:0 auto; padding:0 20px}

/* age banner */
.age-banner{
  background:#20141a; color:#e7b7c1; font-size:.85rem;
  border-bottom:1px solid #3a222c; text-align:center;
  padding:7px 16px;
}

/* header */
.site-header{border-bottom:1px solid var(--line); background:rgba(14,17,22,.9)}
.header-inner{display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; padding:14px 20px}
.brand{font-weight:800; font-size:1.25rem; color:var(--text); text-decoration:none; letter-spacing:.2px; display:flex; flex-direction:column; line-height:1.15}
.brand:hover{color:var(--accent-2)}
.brand-sub{font-size:.68rem; font-weight:500; color:var(--muted); letter-spacing:.4px; text-transform:uppercase}
.site-header nav{display:flex; gap:18px; flex-wrap:wrap; align-items:center}
.site-header nav a{color:var(--muted); text-decoration:none; font-weight:600; font-size:.95rem}
.site-header nav a:hover,.site-header nav a.active{color:var(--text)}
.nav-cta{background:var(--bg-3); border:1px solid var(--line); padding:7px 14px; border-radius:999px; color:var(--text)!important}
.nav-cta:hover{border-color:var(--accent); color:var(--accent-2)!important}

/* hero video */
.hero-video{margin:26px auto 8px; max-width:880px; text-align:center}
.video-frame{
  position:relative; width:100%; aspect-ratio:16/9;
  background:#000; border-radius:var(--radius); overflow:hidden;
  border:1px solid var(--line); box-shadow:0 18px 50px rgba(0,0,0,.45);
}
.video-frame iframe{position:absolute; inset:0; width:100%; height:100%; border:0; display:block}
.hero-video figcaption{margin-top:10px; font-size:.9rem; color:var(--muted)}

/* breadcrumbs */
.breadcrumbs{margin:20px 0 4px; font-size:.85rem; color:var(--muted)}
.breadcrumbs ol{list-style:none; display:flex; gap:8px; flex-wrap:wrap; margin:0; padding:0}
.breadcrumbs li+li::before{content:"\\203a"; margin-right:8px; color:var(--line)}
.breadcrumbs a{color:var(--muted); text-decoration:none}
.breadcrumbs a:hover{color:var(--text)}

/* headings & text */
h1{font-size:clamp(1.55rem,3.5vw,2.3rem); line-height:1.22; margin:14px 0 14px; letter-spacing:-.01em}
h2{font-size:clamp(1.2rem,2.6vw,1.55rem); line-height:1.3; margin:44px 0 12px; letter-spacing:-.01em}
.lede{font-size:1.08rem; color:#c7d0dc; margin:0 0 18px}
section>p, section li, section ol, section ul{margin:0 0 12px}
section ol,section ul{padding-left:22px}
section li{margin-bottom:8px}

/* answer box */
.answer-box{
  background:linear-gradient(180deg,var(--bg-2),var(--bg));
  border:1px solid var(--line); border-left:4px solid var(--ok);
  border-radius:var(--radius); padding:20px 22px; margin:20px 0 8px;
}
.answer-box .spell{font-family:ui-monospace,Menlo,Consolas,monospace; color:#ffd98a; letter-spacing:.08em}
.answer-box p{margin:10px 0}

/* buttons */
.btn{
  display:inline-block; background:var(--bg-3); color:var(--text);
  border:1px solid var(--line); border-radius:999px; padding:12px 22px;
  font-weight:700; font-size:1rem; text-decoration:none; cursor:pointer;
  transition:border-color .15s ease, transform .05s ease;
}
.btn:hover{border-color:var(--accent); transform:translateY(-1px)}
.btn-primary{background:linear-gradient(135deg,#ff4d6d,#ff7a59); border:none; color:#fff; font-size:1.05rem; padding:14px 26px; box-shadow:0 10px 26px rgba(255,77,109,.3)}
.btn-primary:hover{filter:brightness(1.06); color:#fff}
.cta-fineprint{font-size:.8rem; color:var(--muted); margin-top:8px}

/* table */
.table-wrap{overflow-x:auto; border:1px solid var(--line); border-radius:var(--radius); margin:16px 0}
table{border-collapse:collapse; width:100%; min-width:640px; font-size:.95rem}
th,td{padding:12px 14px; text-align:left; border-bottom:1px solid var(--line); vertical-align:top}
thead th{background:var(--bg-2); color:var(--muted); font-size:.8rem; text-transform:uppercase; letter-spacing:.6px}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:none}
tbody th[scope="row"] a{color:var(--accent-2); text-decoration:none}
tbody th[scope="row"] a:hover{color:var(--accent)}
.row-link{font-weight:700; white-space:nowrap}

/* typo grid */
.typo-grid{list-style:none; display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:10px; padding:0; margin:14px 0}
.typo-grid a{
  display:flex; flex-direction:column; gap:3px;
  background:var(--bg-2); border:1px solid var(--line); border-radius:12px;
  padding:12px 14px; text-decoration:none; color:var(--text);
  transition:border-color .15s ease, transform .05s ease;
}
.typo-grid a:hover{border-color:var(--accent); transform:translateY(-2px)}
.typo-grid code{color:var(--accent-2); font-weight:700; background:none; border:none; padding:0; font-size:1rem}
.typo-grid span{font-size:.8rem; color:var(--muted)}

/* cta box */
.cta-box{
  background:linear-gradient(135deg,rgba(255,77,109,.14),rgba(77,163,255,.10));
  border:1px solid rgba(255,77,109,.35); border-radius:var(--radius);
  padding:26px 24px; margin:40px 0;
}
.cta-box h2{margin-top:0}

/* faq */
.faq details{
  background:var(--bg-2); border:1px solid var(--line); border-radius:12px;
  padding:14px 18px; margin-bottom:10px;
}
.faq details[open]{border-color:var(--accent)}
.faq summary{cursor:pointer; font-weight:700; list-style:none; display:flex; gap:10px; align-items:baseline}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:"+"; color:var(--accent); font-weight:800}
.faq details[open] summary::before{content:"\\2013"}
.faq p{margin:10px 0 0; color:#c7d0dc}

/* footer */
.site-footer{border-top:1px solid var(--line); margin-top:56px; padding:28px 20px 34px; color:var(--muted); font-size:.88rem}
.site-footer .about{max-width:760px}
.site-footer .fineprint{font-size:.8rem}
.foot-links a{color:var(--muted); text-decoration:none; font-weight:600}
.foot-links a:hover{color:var(--text)}

/* sticky CTA bar */
.sticky-cta{
  position:fixed; left:0; right:0; bottom:0; z-index:1000;
  background:linear-gradient(90deg,#1a0f14 0%,#241019 100%);
  border-top:2px solid var(--accent);
  padding:10px 14px calc(10px + env(safe-area-inset-bottom));
  box-shadow:0 -12px 34px rgba(0,0,0,.5);
}
.sticky-cta a{
  display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap;
  max-width:920px; margin:0 auto;
  color:#fff; text-decoration:none; font-size:.98rem; line-height:1.3;
}
.sticky-cta .cta-emoji{font-size:1.25rem}
.sticky-cta .cta-text strong{color:var(--accent-2)}
.sticky-cta .cta-url{
  background:rgba(255,77,109,.16); border:1px solid rgba(255,77,109,.5);
  color:var(--accent-2); border-radius:999px; padding:4px 12px;
  font-size:.85rem; font-weight:700; white-space:nowrap;
}
.sticky-cta a:hover .cta-url{background:rgba(255,77,109,.3)}
.sticky-cta a:focus-visible{outline:3px solid var(--accent-2); outline-offset:3px; border-radius:8px}

/* focus & misc */
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--accent); outline-offset:2px; border-radius:6px}
@media (max-width:600px){
  :root{--sticky-h:92px}
  .header-inner{justify-content:center; text-align:center}
  .site-header nav{justify-content:center}
  .video-frame{border-radius:10px}
  .answer-box{padding:16px 16px}
  .sticky-cta{font-size:.9rem}
  .sticky-cta .cta-text{font-size:.88rem}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *{transition:none!important}
}
'''

if __name__ == "__main__":
    build()
