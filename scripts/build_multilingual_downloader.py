#!/usr/bin/env python3
"""
scripts/build_multilingual_downloader.py
Generates 5 dedicated standalone language pages for TheBhom Video Downloader:
  1. English:     downloader/index.html       (https://www.thebhom.in/downloader/)
  2. Hindi:       downloader/hi/index.html    (https://www.thebhom.in/downloader/hi/)
  3. Spanish:     downloader/es/index.html    (https://www.thebhom.in/downloader/es/)
  4. Portuguese:  downloader/pt/index.html    (https://www.thebhom.in/downloader/pt/)
  5. Indonesian:  downloader/id/index.html    (https://www.thebhom.in/downloader/id/)

Every single page has:
  - 100% full-page translation (Head, Meta, Schema, Header, Hero, Input, Results, Trimmer, Guides, FAQs, Reviews, Footer)
  - Native language switcher dropdown that navigates directly to the dedicated page URL
  - Complete Hreflang matrix and canonical tags
  - Schema.org JSON-LD (WebApplication, HowTo, FAQPage) in the native language
"""

import os, json

LANGUAGES = {
    'en': {
        'code': 'en',
        'dir_path': 'downloader/index.html',
        'canonical': 'https://www.thebhom.in/downloader/',
        'html_lang': 'en',
        'og_locale': 'en_US',
        'lang_name': '🇬🇧 English',
        'title': 'All-in-One Video Downloader: Download HD Videos Free | TheBhom',
        'meta_desc': 'Download HD videos & Shorts from YouTube, Instagram Reels, TikTok (No Watermark), Facebook, and Twitter instantly. 100% Free, Fast & No Login Required!',
        'keywords': 'video downloader online, download youtube video 1080p, download instagram reels with audio, tiktok video download without watermark, facebook video download, video to mp3 converter',
        'schema_app_name': 'TheBhom Free Online Video Downloader',
        'schema_app_desc': 'Free high-speed online video downloader to save YouTube videos in 1080p, YouTube Shorts, Instagram Reels with clear audio, TikTok without watermark, and MP3 tracks.',
        'badge': '⚡ Universal Video Downloader Engine',
        'hero_title': 'Free Online All-in-One Video Downloader (Download HD Videos from 40+ Sites)',
        'hero_subtitle': 'Paste any video or reels URL from YouTube, Instagram, TikTok, Facebook, Twitter/X, Pinterest, or Reddit to extract high-definition MP4 clips or MP3 audio tracks instantly.',
        'input_placeholder': 'Paste any video URL (YouTube, Instagram, TikTok, Facebook, Twitter)...',
        'paste_btn': 'Paste',
        'analyze_btn': '🔍 Analyze URL',
        'watch_online_btn': '▶ Watch Online',
        'watch_online_sub': 'Click to play preview instantly',
        'streaming_label': 'Streaming 1080p Full HD',
        'new_tab_btn': '↗ New Tab',
        'close_player_btn': '✕ Close Player',
        'audio_track_label': 'Audio Track',
        'audio_fidelity_label': '320kbps High Fidelity Stereo MP3',
        'formats_title': 'Available Download Formats',
        'formats_sub': 'Click "Play" to stream preview or "Download" to save',
        'trimmer_title': '✂ Precision Clip Trimmer (Optional)',
        'trimmer_sub': 'Cut exact seconds for scene-by-scene clip matching',
        'enable_trimmer': 'Enable Trimmer',
        'start_time': 'Start Time:',
        'end_time': 'End Time:',
        'download_selected_btn': '⬇ Download Selected Format',
        'download_ready': '✅ Download Ready!',
        'save_to_device': 'Save to Device',
        'jump_nav': {
            'yt': '▶️ YouTube Video Download',
            'shorts': '⚡ YouTube Shorts',
            'reels': '📸 Instagram Reels',
            'tiktok': '🎵 TikTok No Watermark',
            'fb': '🌐 Facebook Videos',
            'devices': '📱 iPhone & Android Guide',
            'faqs': '❓ FAQs'
        },
        'guide1': {
            'title': 'How to Download YouTube Videos (Mobile & PC Full HD Guide)',
            'lead': 'Daily millions of educational videos, tutorials, podcast episodes, and music videos are uploaded to YouTube. With TheBhom Video Downloader, save any YouTube video in 1080p Full HD, 720p MP4, or extract pure 320kbps MP3 audio directly without installing any suspicious software or extensions.',
            's1_h': 'Copy YouTube Video Link',
            's1_d': 'Open YouTube in your browser or app, navigate to your desired video, tap the Share icon, and select Copy Link.',
            's2_h': 'Paste URL into TheBhom',
            's2_d': 'Paste the copied URL into the search box above and click the Analyze URL button.',
            's3_h': 'Select Resolution & Download',
            's3_d': 'Choose between 1080p Full HD, 720p MP4, or MP3 Audio, then click Download to save the file directly to your device.',
            'tip': 'Audio Extractor Tip: If you only need background music, speeches, or a podcast episode, select the MP3 Audio format card. It extracts the high-fidelity audio stream, saving your storage and mobile bandwidth.'
        },
        'guide2': {
            'title': 'How to Download YouTube Shorts (Vertical 9:16 High Definition)',
            'lead': 'YouTube Shorts are recorded in a vertical 9:16 aspect ratio. Many legacy online tools incorrectly stretch Shorts into horizontal boxes with black bars. TheBhom detects the native vertical feed to ensure your downloaded Shorts retain crisp, full-screen mobile dimensions.',
            's1_h': 'Copy Short Link',
            's1_d': 'On the YouTube Shorts player, tap the Share button on the right side and click Copy link.',
            's2_h': 'Analyze Instant Stream',
            's2_d': 'Paste the link above and click Analyze. Our serverless CDN resolves the highest available video stream within seconds.',
            's3_h': 'Save to Device Gallery',
            's3_d': 'Click Download to save the uncompressed video without watermarks directly into your phone gallery or computer.'
        },
        'guide3': {
            'title': 'How to Download Instagram Reels with Audio Directly to Gallery',
            'lead': 'The number one issue with online reel downloaders is muted audio or blurred 480p output. TheBhom Downloader packages the original uncompressed 1080p video stream with synchronized AAC High-Definition Stereo Sound, guaranteeing clear music and dialogue every time.',
            's1_h': 'Tap Instagram Share Icon',
            's1_d': 'While viewing the Reel on Instagram, tap the paper plane (Share) icon and select Copy Link.',
            's2_h': 'Paste in TheBhom Downloader',
            's2_d': 'Open thebhom.in/downloader and paste the copied link into the input field.',
            's3_h': 'Instant 1080p Download',
            's3_d': 'Choose 1080p Full HD and hit Download. The video saves directly to your device with full original sound.',
            'tip': 'Public vs Private Reels: TheBhom downloads clips from any public Instagram profile without requiring your login credentials. Never enter your Instagram password into third-party downloading websites.'
        },
        'guide4': {
            'title': 'TikTok Without Watermark & Facebook Video Downloader',
            'lead': 'Content creators and video editors require clean video clips without platform watermarks. TheBhom accesses direct platform CDN streams:',
            'tt_h': '🎵 TikTok No-Watermark MP4',
            'tt_d': 'Paste any TikTok link to receive the original source video without bouncing logos, ready for editing in CapCut, Premiere Pro, or sharing as WhatsApp status.',
            'fb_h': '🌐 Facebook Watch & Reels',
            'fb_d': 'Save clips from Facebook timeline, public group posts, and Facebook Watch in high-bitrate H.264 MP4 for universal compatibility across all media players.'
        },
        'guide5': {
            'title': 'Device Guide: How to Save Videos on Android, iPhone (iOS) & PC',
            'lead': 'Saving files varies across operating systems. Follow these simple steps for your platform:',
            'and_h': '🤖 Android Phones (Samsung, Xiaomi, OnePlus, Vivo)',
            'and_d': 'Paste link in Chrome and tap Download. The file saves directly to your Downloads folder and appears instantly in your Gallery / Google Photos app.',
            'ios_h': '🍏 iPhone & iPad (Safari Secret Trick)',
            'ios_d': 'Tap Download in Safari. Tap the blue arrow in the address bar -> open video -> tap the bottom Share icon -> choose "Save Video". The video moves straight into your Photos / Camera Roll!',
            'pc_h': '💻 Windows PC & Mac (Laptops & Desktops)',
            'pc_d': 'Click Download in Chrome, Edge, or Safari. The file downloads directly to your PC Downloads folder, fully compatible with VLC, Windows Media Player, and QuickTime.'
        },
        'faqs': [
            ('How do I download YouTube videos directly to mobile gallery (Kaise download kare)?', 'Open YouTube, tap Share on any video, and copy the link. Paste it into TheBhom Video Downloader, select 1080p or 720p, and hit Download to save it directly to your smartphone gallery. Read our complete guide: <a href="/guides/youtube-video-kaise-download-kare-gallery-me.html" style="color:var(--dl-primary);font-weight:700;">YouTube Video Kaise Download Kare Guide</a>.'),
            ('Can I download YouTube Shorts without installing an app?', 'Yes! No app installation is required. Simply copy the Shorts link, paste it into TheBhom web tool, and download the original 9:16 vertical HD video in one tap. Tutorial: <a href="/guides/youtube-shorts-video-kaise-download-kare.html" style="color:var(--dl-primary);font-weight:700;">YouTube Shorts Download Guide</a>.'),
            ('How do I download Instagram Reels with audio and no watermark?', 'Copy the Reel link from the Instagram app, paste it into TheBhom, and click Analyze. We fetch the uncompressed MP4 bundled with original AAC stereo audio so your audio is never muted. Guide: <a href="/guides/instagram-reel-gallery-me-audio-ke-sath-kaise-save-kare.html" style="color:var(--dl-primary);font-weight:700;">Instagram Reel Audio Guide</a>.'),
            ('Where do downloaded videos go on an iPhone?', 'On iOS Safari, tap the Downloads arrow in the URL bar after downloading, open the video, tap the Share icon at the bottom left, and choose "Save Video" to send it to your Camera Roll.'),
            ('Does this tool download TikTok videos without a watermark?', 'Yes! TheBhom serverless engine retrieves the clean CDN source stream, delivering pure MP4 video without the floating TikTok logo.'),
            ('Can I convert and extract MP3 audio from a video?', 'Absolutely. Paste any video URL into TheBhom. Among the format cards, select "MP3 Audio" to download a crisp 320kbps audio file directly. Read: <a href="/guides/youtube-se-mp3-song-kaise-download-kare.html" style="color:var(--dl-primary);font-weight:700;">YouTube to MP3 Song Guide</a>.'),
            ('Do I need an account or login to use TheBhom?', 'No! TheBhom is a 100% free online utility. There are zero subscriptions, no sign-ups, and no daily quota limits.'),
            ('Are downloaded MP4 videos compatible with WhatsApp and video editors?', 'Yes. All video downloads are encoded in standard H.264 MP4 format with AAC audio, running seamlessly in WhatsApp, CapCut, Premiere Pro, and VLC.')
        ],
        'nav_deals': 'Deals',
        'nav_downloader': 'Downloader',
        'nav_guides': 'Guides',
        'disclaimer': '⚠️ Disclaimer: TheBhom is a personal media utility and does not host or store copyrighted videos. For personal archiving and educational fair use only.'
    },

    'hi': {
        'code': 'hi',
        'dir_path': 'downloader/hi/index.html',
        'canonical': 'https://www.thebhom.in/downloader/hi/',
        'html_lang': 'hi',
        'og_locale': 'hi_IN',
        'lang_name': '🇮🇳 हिन्दी (Hindi)',
        'title': 'यूनिवर्सल वीडियो डाउनलोडर: मुफ़्त HD वीडियो डाउनलोड करें | TheBhom',
        'meta_desc': 'YouTube, Instagram Reels, TikTok (बिना वॉटरमार्क), Facebook और Twitter से HD वीडियो व MP3 तुरंत डाउनलोड करें। 100% मुफ़्त, तेज़ और बिना लॉगिन!',
        'keywords': 'यूनिवर्सल वीडियो डाउनलोडर, यूट्यूब वीडियो डाउनलोड, यूट्यूब वीडियो डाउनलोड कैसे करें, इंस्टाग्राम रील डाउनलोड, टिकटॉक वीडियो डाउनलोड बिना वॉटरमार्क, फेसबुक वीडियो डाउनलोड, वीडियो से mp3 कन्वर्टर',
        'schema_app_name': 'TheBhom मुफ़्त ऑनलाइन वीडियो डाउनलोडर',
        'schema_app_desc': 'YouTube वीडियो 1080p, YouTube Shorts, साफ़ आवाज़ के साथ Instagram Reels, बिना वॉटरमार्क TikTok और MP3 ऑडियो डाउनलोड करने का मुफ़्त टूल।',
        'badge': '⚡ यूनिवर्सल वीडियो डाउनलोडर इंजन',
        'hero_title': 'मुफ़्त ऑनलाइन ऑल-इन-वन वीडियो डाउनलोडर (40+ साइट्स से HD वीडियो डाउनलोड करें)',
        'hero_subtitle': 'YouTube, Instagram Reels, TikTok, Facebook, Twitter/X, Pinterest या Reddit का कोई भी लिंक पेस्ट करें और हाई-डेफ़िनिशन MP4 वीडियो या MP3 ऑडियो तुरंत सेव करें।',
        'input_placeholder': 'यहाँ किसी भी वीडियो का लिंक पेस्ट करें (YouTube, Instagram, TikTok, Facebook)...',
        'paste_btn': 'पेस्ट करें',
        'analyze_btn': '🔍 लिंक एनालाइज़ करें',
        'watch_online_btn': '▶ ऑनलाइन देखें',
        'watch_online_sub': 'तुरंत प्रीव्यू देखने के लिए क्लिक करें',
        'streaming_label': '1080p Full HD स्ट्रीमिंग चालू है',
        'new_tab_btn': '↗ नए टैब में खोलें',
        'close_player_btn': '✕ प्लेयर बंद करें',
        'audio_track_label': 'ऑडियो ट्रैक',
        'audio_fidelity_label': '320kbps हाई-फ़िडेलिटी स्टीरियो MP3',
        'formats_title': 'उपलब्ध डाउनलोड फ़ॉर्मेट',
        'formats_sub': 'स्ट्रीम करने के लिए "Play" या सेव करने के लिए "Download" पर क्लिक करें',
        'trimmer_title': '✂ प्रिसिजन क्लिप ट्रिमर (वैकल्पिक)',
        'trimmer_sub': 'वीडियो के सटीक सेकंड काटकर छोटा करने के लिए उपयोग करें',
        'enable_trimmer': 'ट्रिमर चालू करें',
        'start_time': 'शुरुआती समय:',
        'end_time': 'समाप्ति समय:',
        'download_selected_btn': '⬇ चुना हुआ फ़ॉर्मेट डाउनलोड करें',
        'download_ready': '✅ डाउनलोड तैयार है!',
        'save_to_device': 'फ़ोन / कंप्यूटर में सेव करें',
        'jump_nav': {
            'yt': '▶️ यूट्यूब वीडियो डाउनलोड',
            'shorts': '⚡ यूट्यूब शॉर्ट्स',
            'reels': '📸 इंस्टाग्राम रील्स',
            'tiktok': '🎵 टिकटॉक बिना वॉटरमार्क',
            'fb': '🌐 फेसबुक वीडियो',
            'devices': '📱 आईफोन व एंड्रॉयड गाइड',
            'faqs': '❓ अक्सर पूछे जाने वाले सवाल'
        },
        'guide1': {
            'title': 'यूट्यूब वीडियो डाउनलोड कैसे करें (मोबाइल और कंप्यूटर पर 1080p Full HD गाइड)',
            'lead': 'यूट्यूब पर प्रतिदिन हज़ारों शैक्षणिक वीडियो, ट्यूटोरियल, पॉडकास्ट और संगीत आते हैं। TheBhom वीडियो डाउनलोडर से आप किसी भी यूट्यूब वीडियो को बिना किसी ऐप या एक्सटेंशन के 1080p Full HD, 720p या डायरेक्ट 320kbps MP3 ऑडियो में डाउनलोड कर सकते हैं।',
            's1_h': 'वीडियो लिंक कॉपी करें',
            's1_d': 'YouTube ऐप या ब्राउज़र में वीडियो खोलें, Share बटन पर टैप करें और Copy Link चुनें।',
            's2_h': 'TheBhom में पेस्ट करें',
            's2_d': 'ऊपर दिए गए सर्च बॉक्स में लिंक पेस्ट करें और Analyze URL बटन पर क्लिक करें।',
            's3_h': 'क्वालिटी चुनें और डाउनलोड करें',
            's3_d': '1080p HD, 720p या MP3 ऑडियो चुनें और सीधे अपनी डिवाइस गैलरी में सेव करें।',
            'tip': 'ऑडियो एक्सट्रैक्टर टिप: अगर आपको सिर्फ भाषण, पॉडकास्ट या गाने का ऑडियो चाहिए, तो MP3 Audio चुनें। इससे वीडियो का शुद्ध ऑडियो अलग होकर आपके मोबाइल का डेटा और स्टोरेज दोनों बचता है।'
        },
        'guide2': {
            'title': 'यूट्यूब शॉर्ट्स डाउनलोड कैसे करें (वर्टिकल 9:16 ओरिजिनल क्वालिटी)',
            'lead': 'YouTube Shorts वर्टिकल 9:16 अनुपात में होते हैं। कई ऑनलाइन टूल शॉर्ट्स के दोनों तरफ काली पट्टियाँ जोड़ देते हैं। TheBhom ओरिजिनल वर्टिकल फ़ीड से वीडियो निकालता है जिससे शॉर्ट्स फुल-स्क्रीन में साफ़ सेव होते हैं।',
            's1_h': 'शॉर्ट का लिंक कॉपी करें',
            's1_d': 'YouTube Shorts फ़ीड में दाईं ओर दिए Share आइकन पर टैप करके Copy link करें।',
            's2_h': 'फ़ास्ट एनालाइज़र में डालें',
            's2_d': 'लिंक यहाँ पेस्ट करके एनालाइज़ करें। हमारा सर्वरलेस इंजन 1-2 सेकंड में बेस्ट क्वालिटी फेच कर लेता है।',
            's3_h': 'गैलरी में सीधे सेव करें',
            's3_d': 'Download पर क्लिक करते ही बिना किसी वॉटरमार्क के ओरिजिनल वीडियो गैलरी में सेव हो जाएगी।'
        },
        'guide3': {
            'title': 'इंस्टाग्राम रील ऑडियो के साथ गैलरी में कैसे डाउनलोड करें',
            'lead': 'इंस्टाग्राम रील्स डाउनलोड करते समय सबसे बड़ी समस्या आवाज़ बंद (म्यूट) होने की होती है। TheBhom ओरिजिनल 1080p वीडियो के साथ-साथ ओरिजिनल AAC स्टीरियो साउंड को जोड़कर MP4 प्रदान करता है, जिससे पूरी आवाज़ साफ़ सुनाई देती है।',
            's1_h': 'रील का शेयर आइकन दबाएँ',
            's1_d': 'Instagram ऐप में रील देखते समय Share आइकन पर क्लिक करें और Copy Link चुनें।',
            's2_h': 'TheBhom में लिंक पेस्ट करें',
            's2_d': 'thebhom.in/downloader/hi खोलें और सर्च बॉक्स में लिंक पेस्ट करके एनालाइज़ करें।',
            's3_h': 'आवाज़ के साथ 1080p में सेव करें',
            's3_d': '1080p HD चुनें और डाउनलोड दबाएँ। पूरी साउंडट्रैक के साथ वीडियो सीधे गैलरी में आ जाएगी।',
            'tip': 'सुरक्षा चेतावनी: TheBhom किसी भी पब्लिक प्रोफ़ाइल की रील बिना पासवर्ड माँगे डाउनलोड करता है। किसी भी वेबसाइट पर अपना इंस्टाग्राम पासवर्ड कभी न डालें।'
        },
        'guide4': {
            'title': 'बिना वॉटरमार्क टिकटॉक व फेसबुक वीडियो डाउनलोडर',
            'lead': 'वीडियो एडिटर्स और क्रिएटर्स को बिना वॉटरमार्क वाले साफ़ वीडियो चाहिए होते हैं। TheBhom डायरेक्ट सोर्स से वीडियो फेच करता है:',
            'tt_h': '🎵 टिकटॉक नो-वॉटरमार्क MP4',
            'tt_d': 'टिकटॉक का लिंक पेस्ट करते ही बिना किसी लोगो वाला ओरिजिनल वीडियो मिलता है, जिसे आप CapCut, Premiere Pro या WhatsApp स्टेटस में उपयोग कर सकते हैं।',
            'fb_h': '🌐 फेसबुक वीडियो व रील्स',
            'fb_d': 'फेसबुक टाइमलाइन, ग्रुप्स और FB Watch के वीडियो को हाई-बिटरेट MP4 में सेव करें जो सभी मीडिया प्लेयर्स में बिना रुके चलता है।'
        },
        'guide5': {
            'title': 'डिवाइस गाइड: एंड्रॉयड, आईफोन (iOS) और कंप्यूटर में वीडियो कैसे सेव करें',
            'lead': 'अलग-अलग ऑपरेटिंग सिस्टम में फाइल सेव करने के आसान और व्यावहारिक तरीके:',
            'and_h': '🤖 एंड्रॉयड फ़ोन (सैमसंग, रेडमी, वनप्लस, वीवो, रियलमी)',
            'and_d': 'Chrome ब्राउज़र में लिंक पेस्ट करके Download दबाएँ। फ़ाइल तुरंत फ़ोन के Downloads फ़ोल्डर में जाकर Gallery और Google Photos में दिखने लगेगी।',
            'ios_h': '🍏 आईफ़ोन व आईपैड (Safari का आसान तरीका)',
            'ios_d': 'Safari में Download दबाने पर ऊपर नीला तीर (डाउनलोड्स) दिखेगा। उस पर टैप करें -> वीडियो खोलें -> नीचे बाएँ कोने में Share आइकन दबाएँ -> "Save Video" चुनें। वीडियो तुरंत Photos ऐप / कैमरा रोल में पहुँच जाएगी!',
            'pc_h': '💻 विंडोज़ कंप्यूटर व मैक (लैपटॉप और डेस्कटॉप)',
            'pc_d': 'Chrome या Safari में Download पर क्लिक करते ही वीडियो सीधे कंप्यूटर के Downloads फ़ोल्डर में सुरक्षित हो जाती है।'
        },
        'faqs': [
            ('यूट्यूब वीडियो कैसे डाउनलोड करें (YouTube Video Kaise Download Kare)?', 'YouTube ऐप में वीडियो का Link Copy करें, TheBhom में पेस्ट करके Download बटन दबाएँ। वीडियो सीधे आपके मोबाइल की Gallery और File Manager में Save हो जाएगी। विस्तार से समझने के लिए पढ़ें: <a href="/guides/youtube-video-kaise-download-kare-gallery-me.html" style="color:var(--dl-primary);font-weight:700;">YouTube Video Kaise Download Kare Full Guide</a>'),
            ('Dawnload kese kre youtube video direct phone ki gallery me?', 'YouTube video ko direct phone gallery me download karne ke liye kisi third-party app ki zaroorat nahi hai. TheBhom.in par aakar link paste karein aur 1080p ya 720p chunein, video 1-click me save ho jayegi.'),
            ('Mujhe youtube video chahiye direct file me, kaise download karu?', 'TheBhom aapko standard MP4 file format me direct video download deta hai, jise aap offline bina internet kisi bhi media player (VLC, MX Player) me chala sakte hain aur WhatsApp par share kar sakte hain.'),
            ('Kese kre youtube shot damnlod bina kisi app ke?', 'YouTube Shorts video ke Share icon par jakar "Copy link" karein, TheBhom me paste karein aur Download dabayein. Shorts 9:16 vertical full HD me save ho jayegi. Step-by-step padhein: <a href="/guides/youtube-shorts-video-kaise-download-kare.html" style="color:var(--dl-primary);font-weight:700;">YouTube Shorts Download Guide</a>'),
            ('Instagram reel direct gallery me save kaise kare audio ke sath?', 'Instagram Reel link copy karke TheBhom me paste karein. Hamara tool original video aur background music ko combine karke bina watermark ke gallery me save karta hai. Pura process padhein: <a href="/guides/instagram-reel-gallery-me-audio-ke-sath-kaise-save-kare.html" style="color:var(--dl-primary);font-weight:700;">Instagram Reel Audio Fix Guide</a>'),
            ('YouTube se MP3 gana / song kaise download kare?', 'Agar aapko video ka sirf gana ya audio chahiye, toh TheBhom me link paste karke "MP3 Audio" select karein. Yeh 320kbps high clarity me song download kar deta hai. Guide: <a href="/guides/youtube-se-mp3-song-kaise-download-kare.html" style="color:var(--dl-primary);font-weight:700;">YouTube to MP3 Song Guide</a>'),
            ('क्या डाउनलोड वीडियो पर कोई वॉटरमार्क या लोगो आता है?', 'नहीं, TheBhom से डाउनलोड किए गए किसी भी वीडियो या रील पर कोई वॉटरमार्क, लोगो या यूजरनेम नहीं आता है।'),
            ('आईफ़ोन (iOS) और एंड्रॉयड में वीडियो कहाँ सेव होती है?', 'Android में यह Downloads फोल्डर व Gallery में आती है। iPhone में Safari के Downloads से शेयर करके "Save Video" दबाने पर Photos (Camera Roll) में सेव हो जाती है।')
        ],
        'nav_deals': 'डील्स',
        'nav_downloader': 'डाउनलोडर',
        'nav_guides': 'गाइड्स',
        'disclaimer': '⚠️ अस्वीकरण: TheBhom एक व्यक्तिगत मीडिया एक्सट्रैक्शन टूल है और अपने सर्वर पर कोई कॉपीराइट वीडियो स्टोर नहीं करता। केवल निजी अध्ययन व फ़ेयर यूज़ के लिए।'
    },

    'es': {
        'code': 'es',
        'dir_path': 'downloader/es/index.html',
        'canonical': 'https://www.thebhom.in/downloader/es/',
        'html_lang': 'es',
        'og_locale': 'es_ES',
        'lang_name': '🇪🇸 Español (Spanish)',
        'title': 'Descargador Universal de Videos: Descargar Videos HD Gratis | TheBhom',
        'meta_desc': 'Descarga videos y Shorts en HD de YouTube, Instagram Reels, TikTok (sin marca de agua), Facebook y Twitter al instante. 100% Gratis, Rápido y Sin Registro.',
        'keywords': 'descargador de videos online, descargar videos de youtube 1080p, descargar reels de instagram con audio, descargar tiktok sin marca de agua, descargar videos de facebook, convertir video a mp3',
        'schema_app_name': 'TheBhom Descargador de Videos Online Gratis',
        'schema_app_desc': 'Herramienta gratuita para descargar videos de YouTube en 1080p, Shorts, Reels de Instagram con audio claro, TikTok sin marca de agua y pistas MP3.',
        'badge': '⚡ Motor Universal de Descarga de Videos',
        'hero_title': 'Descargador de Videos Online Todo en Uno (Descarga en HD de 40+ Sitios)',
        'hero_subtitle': 'Pega cualquier enlace de YouTube, Instagram Reels, TikTok, Facebook, Twitter/X, Pinterest o Reddit para extraer clips MP4 en alta definición o pistas MP3 al instante.',
        'input_placeholder': 'Pega la URL del video aquí (YouTube, Instagram, TikTok, Facebook)...',
        'paste_btn': 'Pegar',
        'analyze_btn': '🔍 Analizar Enlace',
        'watch_online_btn': '▶ Ver Online',
        'watch_online_sub': 'Haz clic para previsualizar al instante',
        'streaming_label': 'Transmitiendo en 1080p Full HD',
        'new_tab_btn': '↗ Abrir en Nueva Pestaña',
        'close_player_btn': '✕ Cerrar Reproductor',
        'audio_track_label': 'Pista de Audio',
        'audio_fidelity_label': 'MP3 Estéreo de Alta Fidelidad a 320kbps',
        'formats_title': 'Formatos de Descarga Disponibles',
        'formats_sub': 'Haz clic en "Play" para transmitir o en "Download" para guardar',
        'trimmer_title': '✂ Cortador de Precisión de Video (Opcional)',
        'trimmer_sub': 'Corta segundos exactos para edición y sincronización de escenas',
        'enable_trimmer': 'Activar Cortador',
        'start_time': 'Tiempo Inicial:',
        'end_time': 'Tiempo Final:',
        'download_selected_btn': '⬇ Descargar Formato Seleccionado',
        'download_ready': '✅ ¡Descarga Lista!',
        'save_to_device': 'Guardar en Dispositivo',
        'jump_nav': {
            'yt': '▶️ Descargar de YouTube',
            'shorts': '⚡ YouTube Shorts',
            'reels': '📸 Instagram Reels',
            'tiktok': '🎵 TikTok Sin Marca',
            'fb': '🌐 Videos de Facebook',
            'devices': '📱 Guía iPhone y Android',
            'faqs': '❓ Preguntas Frecuentes'
        },
        'guide1': {
            'title': 'Cómo Descargar Videos de YouTube (Guía Full HD para Móvil y PC)',
            'lead': 'Cada día se suben millones de videos a YouTube. Con TheBhom Video Downloader puedes guardar cualquier video en 1080p Full HD, 720p MP4 o extraer audio MP3 a 320kbps sin instalar programas ni extensiones sospechosas.',
            's1_h': 'Copia el Enlace de YouTube',
            's1_d': 'Abre YouTube en la app o navegador, busca el video deseado, toca en Compartir y selecciona Copiar enlace.',
            's2_h': 'Pega el Enlace en TheBhom',
            's2_d': 'Pega la URL copiada en el cuadro de búsqueda superior y haz clic en Analizar Enlace.',
            's3_h': 'Elige la Calidad y Descarga',
            's3_d': 'Selecciona 1080p Full HD, 720p o audio MP3 y haz clic en Descargar para guardarlo directamente en tu dispositivo.',
            'tip': 'Consejo para Extraer Audio: Si solo necesitas la música o un podcast, elige la tarjeta MP3 Audio para ahorrar datos y espacio en tu teléfono.'
        },
        'guide2': {
            'title': 'Cómo Descargar YouTube Shorts (Formato Vertical 9:16 en Alta Definición)',
            'lead': 'Los Shorts de YouTube se graban en formato vertical 9:16. Muchas herramientas antiguas estiran los Shorts y agregan barras negras. TheBhom extrae el feed original para que tu video se guarde en pantalla completa nítida.',
            's1_h': 'Copia el Enlace del Short',
            's1_d': 'En el reproductor de Shorts, toca el icono de Compartir a la derecha y selecciona Copiar enlace.',
            's2_h': 'Analiza con Servidores Rápidos',
            's2_d': 'Pega el enlace arriba y haz clic en Analizar. Nuestro motor obtiene la máxima resolución en segundos.',
            's3_h': 'Guarda en la Galería',
            's3_d': 'Haz clic en Descargar para guardar el video limpio sin marcas de agua en tu teléfono o computadora.'
        },
        'guide3': {
            'title': 'Cómo Descargar Instagram Reels con Audio en la Galería',
            'lead': 'El problema más común al descargar Reels es que la música o el audio se silencian. TheBhom combina la transmisión de video 1080p con audio estéreo AAC original, garantizando que el sonido se escuche perfecto.',
            's1_h': 'Toca el Icono de Compartir',
            's1_d': 'En Instagram, mientras ves el Reel, toca el icono de compartir y selecciona Copiar enlace.',
            's2_h': 'Pega en TheBhom Downloader',
            's2_d': 'Ingresa a thebhom.in/downloader/es y pega el enlace en el cuadro de búsqueda.',
            's3_h': 'Descarga en 1080p con Sonido',
            's3_d': 'Elige 1080p y presiona Descargar. El video se guardará con toda la música directamente en tu galería.',
            'tip': 'Seguridad y Privacidad: TheBhom descarga de cualquier cuenta pública sin solicitar contraseñas. Nunca ingreses tus claves de Instagram en sitios web externos.'
        },
        'guide4': {
            'title': 'TikTok Sin Marca de Agua y Descargador de Facebook',
            'lead': 'Los creadores de contenido y editores necesitan clips limpios sin logotipos saltarines. TheBhom obtiene los archivos directamente de los servidores de origen:',
            'tt_h': '🎵 TikTok Sin Marca de Agua MP4',
            'tt_d': 'Pega cualquier enlace de TikTok para obtener el video original sin el logotipo flotante, listo para editar en CapCut o compartir en tus estados.',
            'fb_h': '🌐 Facebook Watch y Reels',
            'fb_d': 'Descarga videos de noticias, grupos públicos y Facebook Watch en MP4 estándar H.264 para reproducción fluida en cualquier dispositivo.'
        },
        'guide5': {
            'title': 'Guía por Dispositivo: Cómo Guardar en Android, iPhone (iOS) y PC',
            'lead': 'Guardar archivos cambia según el sistema operativo. Sigue estas instrucciones paso a paso:',
            'and_h': '🤖 Teléfonos Android (Samsung, Xiaomi, Motorola, etc.)',
            'and_d': 'Pega el enlace en Chrome y pulsa Descargar. El archivo se guardará en la carpeta Descargas y aparecerá en tu app de Galería o Google Fotos.',
            'ios_h': '🍏 iPhone y iPad (Truco de Safari)',
            'ios_d': 'En Safari, pulsa Descargar. Toca la flecha azul de descargas en la barra superior -> abre el video -> toca el icono Compartir abajo a la izquierda -> selecciona "Guardar Video". ¡Listo en tu app Fotos / Carrete!',
            'pc_h': '💻 Computadoras Windows y Mac',
            'pc_d': 'Haz clic en Descargar en Chrome, Edge o Safari. El archivo irá directo a tu carpeta de Descargas, compatible con VLC y Windows Media Player.'
        },
        'faqs': [
            ('1. ¿Cómo descargo videos de YouTube en el celular?', 'Abre YouTube, toca Compartir en el video y copia el enlace. Pégalo en TheBhom, haz clic en Analizar, elige 1080p o 720p y presiona Descargar para guardarlo en tu teléfono.'),
            ('2. ¿Puedo descargar YouTube Shorts sin instalar apps?', '¡Sí! No necesitas instalar nada. Simplemente copia el enlace del Short, pégalo en TheBhom y descárgalo en formato vertical 9:16 con un solo clic.'),
            ('3. ¿Cómo descargo un Reel de Instagram con música?', 'TheBhom vincula el video 1080p con el audio original AAC estéreo, garantizando que el audio y la música nunca se silencien.'),
            ('4. ¿Dónde se guardan los videos descargados en iPhone?', 'En Safari, toca la flecha azul de descargas arriba, abre el video, pulsa el botón Compartir y elige "Guardar Video" para enviarlo al Carrete de Fotos.'),
            ('5. ¿Se descargan los videos de TikTok sin marca de agua?', 'Sí. Nuestro motor obtiene el archivo fuente directo del servidor, eliminando por completo el logotipo flotante de TikTok.'),
            ('6. ¿Puedo extraer la música o audio MP3 de un video?', 'Totalmente. Pega cualquier video en TheBhom y en los formatos disponibles selecciona "MP3 Audio" para descargar un archivo a 320kbps.'),
            ('7. ¿Necesito registrarme o pagar para usar TheBhom?', 'No. TheBhom es 100% gratuito, sin suscripciones, sin registro y sin límites diarios.'),
            ('8. ¿Los videos MP4 funcionan en WhatsApp y editores?', 'Sí. Todos los videos están codificados en formato estándar H.264 con audio AAC, compatibles con WhatsApp, CapCut, Premiere y VLC.')
        ],
        'nav_deals': 'Ofertas',
        'nav_downloader': 'Descargador',
        'nav_guides': 'Guías',
        'disclaimer': '⚠️ Aviso Legal: TheBhom es una herramienta de extracción multimedia personal y no aloja videos protegidos por derechos de autor. Solo para uso personal y educativo.'
    },

    'pt': {
        'code': 'pt',
        'dir_path': 'downloader/pt/index.html',
        'canonical': 'https://www.thebhom.in/downloader/pt/',
        'html_lang': 'pt',
        'og_locale': 'pt_BR',
        'lang_name': '🇧🇷 Português (Portuguese)',
        'title': 'Baixador Universal de Vídeos: Baixar Vídeos HD Grátis | TheBhom',
        'meta_desc': 'Baixe vídeos e Shorts em HD do YouTube, Instagram Reels, TikTok (sem marca d\'água), Facebook e Twitter instantaneamente. 100% Grátis, Rápido e Sem Cadastro.',
        'keywords': 'baixar videos online, baixar video do youtube 1080p, baixar reels do instagram com audio, baixar tiktok sem marca dagua, baixar videos do facebook, conversor de video para mp3',
        'schema_app_name': 'TheBhom Baixador de Vídeos Online Grátis',
        'schema_app_desc': 'Ferramenta online gratuita para baixar vídeos do YouTube em 1080p, Shorts, Reels do Instagram com áudio nítido, TikTok sem marca d\'água e músicas em MP3.',
        'badge': '⚡ Motor Universal de Download de Vídeos',
        'hero_title': 'Baixador de Vídeos Online Tudo-em-Um (Baixe em HD de Mais de 40 Sites)',
        'hero_subtitle': 'Cole qualquer link do YouTube, Instagram Reels, TikTok, Facebook, Twitter/X, Pinterest ou Reddit para extrair vídeos MP4 em alta definição ou faixas MP3 instantaneamente.',
        'input_placeholder': 'Cole a URL do vídeo aqui (YouTube, Instagram, TikTok, Facebook)...',
        'paste_btn': 'Colar',
        'analyze_btn': '🔍 Analisar Link',
        'watch_online_btn': '▶ Assistir Online',
        'watch_online_sub': 'Clique para pré-visualizar instantaneamente',
        'streaming_label': 'Transmitindo em 1080p Full HD',
        'new_tab_btn': '↗ Nova Aba',
        'close_player_btn': '✕ Fechar Player',
        'audio_track_label': 'Faixa de Áudio',
        'audio_fidelity_label': 'MP3 Estéreo de Alta Fidelidade a 320kbps',
        'formats_title': 'Formatos de Download Disponíveis',
        'formats_sub': 'Clique em "Play" para reproduzir ou em "Download" para salvar',
        'trimmer_title': '✂ Cortador Preciso de Clipes (Opcional)',
        'trimmer_sub': 'Corte trechos exatos em segundos para edição de vídeos',
        'enable_trimmer': 'Ativar Cortador',
        'start_time': 'Início:',
        'end_time': 'Fim:',
        'download_selected_btn': '⬇ Baixar Formato Selecionado',
        'download_ready': '✅ Download Pronto!',
        'save_to_device': 'Salvar no Dispositivo',
        'jump_nav': {
            'yt': '▶️ Baixar do YouTube',
            'shorts': '⚡ YouTube Shorts',
            'reels': '📸 Instagram Reels',
            'tiktok': '🎵 TikTok Sem Marca',
            'fb': '🌐 Vídeos do Facebook',
            'devices': '📱 Guia iPhone e Android',
            'faqs': '❓ Perguntas Frequentes'
        },
        'guide1': {
            'title': 'Como Baixar Vídeos do YouTube (Guia Full HD para Celular e PC)',
            'lead': 'Milhões de vídeos educativos, podcasts e músicas são publicados no YouTube diariamente. Com o TheBhom Video Downloader, você salva qualquer vídeo em 1080p Full HD, 720p MP4 ou extrai o áudio MP3 em 320kbps sem instalar programas ou extensões suspeitas.',
            's1_h': 'Copie o Link do YouTube',
            's1_d': 'Abra o YouTube no app ou navegador, acesse o vídeo, clique em Compartilhar e selecione Copiar link.',
            's2_h': 'Cole o Link no TheBhom',
            's2_d': 'Cole a URL copiada no campo de busca acima e clique no botão Analisar Link.',
            's3_h': 'Escolha a Resolução e Baixe',
            's3_d': 'Selecione 1080p Full HD, 720p ou áudio MP3 e clique em Baixar para salvar diretamente no seu aparelho.',
            'tip': 'Dica de Áudio MP3: Se você só precisa da música ou do podcast, escolha o formato MP3 Audio para economizar espaço de armazenamento e dados móveis.'
        },
        'guide2': {
            'title': 'Como Baixar YouTube Shorts (Formato Vertical 9:16 em Alta Definição)',
            'lead': 'Os Shorts do YouTube são gravados no formato vertical 9:16. Muitas ferramentas esticam o vídeo e colocam faixas pretas. O TheBhom detecta o stream original para que seu vídeo seja salvo em tela cheia com máxima nitidez.',
            's1_h': 'Copie o Link do Short',
            's1_d': 'No player de Shorts, clique no ícone de Compartilhar à direita e selecione Copiar link.',
            's2_h': 'Análise Instantânea',
            's2_d': 'Cole o link acima e clique em Analisar. Nossos servidores identificam a melhor resolução em segundos.',
            's3_h': 'Salvar na Galeria',
            's3_d': 'Clique em Baixar para salvar o vídeo limpo e sem marcas d\'água no celular ou computador.'
        },
        'guide3': {
            'title': 'Como Baixar Reels do Instagram com Áudio na Galeria',
            'lead': 'A principal queixa de quem baixa Reels é que a música ou a voz ficam mudas. O TheBhom combina o vídeo em 1080p com o áudio estéreo AAC original, garantindo que o som seja reproduzido com perfeição.',
            's1_h': 'Toque no Ícone de Compartilhar',
            's1_d': 'No app do Instagram, enquanto assiste ao Reel, toque no aviãozinho de papel e clique em Copiar link.',
            's2_h': 'Cole no TheBhom Downloader',
            's2_d': 'Acesse thebhom.in/downloader/pt e cole o link no campo de busca.',
            's3_h': 'Download em 1080p com Som',
            's3_d': 'Escolha 1080p e clique em Baixar. O vídeo será salvo na galeria com a trilha sonora completa.',
            'tip': 'Segurança em Primeiro Lugar: O TheBhom faz o download de qualquer perfil público sem pedir senhas. Nunca digite sua senha do Instagram em sites de terceiros.'
        },
        'guide4': {
            'title': 'TikTok Sem Marca d\'Água e Baixador do Facebook',
            'lead': 'Criadores de conteúdo e editores precisam de clipes limpos sem logotipos móveis. O TheBhom baixa diretamente dos servidores de origem:',
            'tt_h': '🎵 TikTok Sem Marca d\'Água MP4',
            'tt_d': 'Cole o link do TikTok para receber o vídeo original sem a marca flutuante, pronto para edição no CapCut ou publicação no status do WhatsApp.',
            'fb_h': '🌐 Vídeos do Facebook e Reels',
            'fb_d': 'Baixe vídeos da linha do tempo, grupos públicos e Facebook Watch em MP4 H.264 para reprodução suave em qualquer reprodutor.'
        },
        'guide5': {
            'title': 'Guia por Aparelho: Como Salvar no Android, iPhone (iOS) e PC',
            'lead': 'O salvamento de arquivos varia em cada sistema. Siga o passo a passo para o seu dispositivo:',
            'and_h': '🤖 Celulares Android (Samsung, Motorola, Xiaomi, etc.)',
            'and_d': 'Cole o link no Google Chrome e toque em Baixar. O arquivo irá para a pasta Downloads e aparecerá no app Galeria ou Google Fotos.',
            'ios_h': '🍏 iPhone e iPad (Truque Prático do Safari)',
            'ios_d': 'No Safari, toque em Baixar. Toque na seta azul de downloads na barra superior -> abra o vídeo -> toque no ícone de Compartilhar no canto inferior esquerdo -> selecione "Salvar Vídeo". Pronto, salvo no app Fotos / Rolo da Câmera!',
            'pc_h': '💻 Computadores Windows e Mac',
            'pc_d': 'Clique em Baixar no Chrome, Edge ou Safari. O arquivo irá direto para a pasta Downloads, compatível com VLC e Windows Media Player.'
        },
        'faqs': [
            ('1. Como baixar vídeos do YouTube no celular?', 'Abra o YouTube, toque em Compartilhar e copie o link. Cole no TheBhom, clique em Analisar, escolha 1080p ou 720p e toque em Baixar para salvar no smartphone.'),
            ('2. Posso baixar YouTube Shorts sem instalar aplicativos?', 'Sim! Não requer aplicativo. Copie o link do Short, cole no TheBhom e faça o download no formato vertical 9:16 com um clique.'),
            ('3. Como baixar Reels do Instagram com áudio e música?', 'O TheBhom combina o arquivo MP4 em 1080p com a faixa de áudio estéreo AAC original, garantindo que o som nunca fique mudo.'),
            ('4. Onde ficam os vídeos baixados no iPhone?', 'No Safari, toque na seta azul de downloads acima, abra o arquivo, clique em Compartilhar e selecione "Salvar Vídeo" para enviar ao Rolo da Câmera.'),
            ('5. O TheBhom baixa vídeos do TikTok sem marca d\'água?', 'Sim! Nosso sistema busca o arquivo fonte original, removendo completamente o logotipo flutuante do TikTok.'),
            ('6. É possível extrair o áudio MP3 de um vídeo?', 'Sim. Cole qualquer link de vídeo no TheBhom e selecione "MP3 Audio" nas opções para baixar a faixa sonora em 320kbps.'),
            ('7. Preciso fazer login ou pagar para usar o TheBhom?', 'Não. O TheBhom é 100% gratuito, sem mensalidade, sem cadastro e sem limites diários de download.'),
            ('8. Os vídeos em MP4 funcionam no WhatsApp e editores?', 'Sim. Todos os downloads usam a codificação H.264 com áudio AAC, funcionando perfeitamente no WhatsApp, CapCut, Premiere e VLC.')
        ],
        'nav_deals': 'Ofertas',
        'nav_downloader': 'Baixador',
        'nav_guides': 'Guias',
        'disclaimer': '⚠️ Aviso Legal: O TheBhom é uma ferramenta para uso pessoal e não hospeda vídeos protegidos por direitos autorais em seus servidores.'
    },

    'id': {
        'code': 'id',
        'dir_path': 'downloader/id/index.html',
        'canonical': 'https://www.thebhom.in/downloader/id/',
        'html_lang': 'id',
        'og_locale': 'id_ID',
        'lang_name': '🇮🇩 Bahasa Indonesia',
        'title': 'Pengunduh Video Universal: Unduh Video HD Gratis | TheBhom',
        'meta_desc': 'Unduh video & Shorts HD dari YouTube, Instagram Reels, TikTok (tanpa watermark), Facebook, dan Twitter secara instan. 100% Gratis, Cepat & Tanpa Login!',
        'keywords': 'download video online, download video youtube 1080p, download reels instagram dengan suara, download tiktok tanpa watermark, download video facebook, konverter video ke mp3',
        'schema_app_name': 'TheBhom Pengunduh Video Online Gratis',
        'schema_app_desc': 'Alat online gratis berkecepatan tinggi untuk mengunduh video YouTube 1080p, Shorts, Reels Instagram dengan suara jernih, TikTok tanpa watermark, dan lagu MP3.',
        'badge': '⚡ Mesin Pengunduh Video Universal',
        'hero_title': 'Pengunduh Video Online Serbaguna Gratis (Unduh Video HD dari 40+ Situs)',
        'hero_subtitle': 'Tempelkan URL video atau reels dari YouTube, Instagram, TikTok, Facebook, Twitter/X, Pinterest, atau Reddit untuk mengekstrak klip MP4 beresolusi tinggi atau trek audio MP3 secara instan.',
        'input_placeholder': 'Tempel tautan video di sini (YouTube, Instagram, TikTok, Facebook)...',
        'paste_btn': 'Tempel',
        'analyze_btn': '🔍 Analisis URL',
        'watch_online_btn': '▶ Tonton Online',
        'watch_online_sub': 'Klik untuk memutar pratinjau instan',
        'streaming_label': 'Streaming 1080p Full HD Aktif',
        'new_tab_btn': '↗ Buka Tab Baru',
        'close_player_btn': '✕ Tutup Pemutar',
        'audio_track_label': 'Trek Audio',
        'audio_fidelity_label': 'MP3 Stereo Kesetiaan Tinggi 320kbps',
        'formats_title': 'Format Unduhan yang Tersedia',
        'formats_sub': 'Klik "Play" untuk memutar pratinjau atau "Download" untuk menyimpan',
        'trimmer_title': '✂ Pemotong Klip Presisi (Opsional)',
        'trimmer_sub': 'Potong detik video secara akurat untuk kebutuhan konten Anda',
        'enable_trimmer': 'Aktifkan Pemotong',
        'start_time': 'Waktu Mulai:',
        'end_time': 'Waktu Selesai:',
        'download_selected_btn': '⬇ Unduh Format yang Dipilih',
        'download_ready': '✅ Unduhan Siap!',
        'save_to_device': 'Simpan ke Perangkat',
        'jump_nav': {
            'yt': '▶️ Unduh YouTube',
            'shorts': '⚡ YouTube Shorts',
            'reels': '📸 Instagram Reels',
            'tiktok': '🎵 TikTok Tanpa Watermark',
            'fb': '🌐 Video Facebook',
            'devices': '📱 Panduan iPhone & Android',
            'faqs': '❓ Tanya Jawab'
        },
        'guide1': {
            'title': 'Cara Mengunduh Video YouTube (Panduan Full HD untuk Ponsel & PC)',
            'lead': 'Setiap hari jutaan video edukasi, tutorial, dan podcast diunggah ke YouTube. Dengan TheBhom Video Downloader, Anda dapat mengunduh video apa pun dalam kualitas 1080p Full HD, 720p MP4, atau mengekstrak audio MP3 320kbps tanpa perlu memasang aplikasi atau ekstensi apa pun.',
            's1_h': 'Salin Tautan Video YouTube',
            's1_d': 'Buka aplikasi atau situs YouTube, pilih video yang diinginkan, ketuk Bagikan (Share), lalu pilih Salin Tautan (Copy Link).',
            's2_h': 'Tempel Tautan di TheBhom',
            's2_d': 'Tempelkan URL yang telah disalin ke kotak pencarian di atas dan klik tombol Analisis URL.',
            's3_h': 'Pilih Resolusi & Unduh',
            's3_d': 'Pilih resolusi 1080p Full HD, 720p, atau audio MP3, lalu klik Unduh untuk menyimpan langsung ke perangkat Anda.',
            'tip': 'Tips Ekstraksi Audio: Jika Anda hanya memerlukan musik latar atau podcast, pilih format MP3 Audio untuk menghemat kuota internet dan ruang memori ponsel Anda.'
        },
        'guide2': {
            'title': 'Cara Mengunduh YouTube Shorts (Format Vertikal 9:16 Kualitas Asli)',
            'lead': 'YouTube Shorts direkam dalam format vertikal 9:16. Banyak situs web mengubahnya menjadi kotak horizontal dengan garis hitam. TheBhom mengambil feed asli sehingga video Shorts Anda tersimpan dalam layar penuh tanpa penurunan kualitas.',
            's1_h': 'Salin Tautan Shorts',
            's1_d': 'Di pemutar YouTube Shorts, ketuk ikon Bagikan di sebelah kanan dan pilih Salin tautan.',
            's2_h': 'Analisis Server Cepat',
            's2_d': 'Tempel tautan di atas dan klik Analisis. Sistem kami akan menemukan resolusi terbaik dalam hitungan detik.',
            's3_h': 'Simpan ke Galeri Ponsel',
            's3_d': 'Klik Unduh untuk menyimpan video jernih tanpa watermark langsung ke galeri ponsel Anda.'
        },
        'guide3': {
            'title': 'Cara Mengunduh Reels Instagram dengan Suara ke Galeri',
            'lead': 'Masalah paling sering saat mengunduh Reels adalah suara atau musiknya hilang (bisu). TheBhom Downloader menggabungkan video 1080p dengan suara stereo AAC asli, sehingga audio terdengar jernih tanpa cacat.',
            's1_h': 'Ketuk Ikon Bagikan di Reels',
            's1_d': 'Saat menonton Reels di aplikasi Instagram, ketuk ikon pesawat kertas lalu pilih Salin Tautan.',
            's2_h': 'Tempelkan di TheBhom Downloader',
            's2_d': 'Buka thebhom.in/downloader/id dan tempelkan tautan ke kolom pencarian.',
            's3_h': 'Unduh 1080p dengan Musik Penuh',
            's3_d': 'Pilih kualitas 1080p dan klik Unduh. Video akan tersimpan langsung ke galeri dengan lagu lengkap.',
            'tip': 'Keamanan Data: TheBhom mengunduh dari akun publik tanpa meminta kata sandi. Jangan pernah memasukkan kata sandi akun Instagram Anda di situs web mana pun.'
        },
        'guide4': {
            'title': 'TikTok Tanpa Watermark & Pengunduh Video Facebook',
            'lead': 'Kreator konten dan editor video membutuhkan klip bersih tanpa logo mengambang. TheBhom mengambil video langsung dari server CDN asli:',
            'tt_h': '🎵 TikTok MP4 Tanpa Watermark',
            'tt_d': 'Tempel tautan TikTok apa pun untuk mendapatkan video asli tanpa logo bergerak, siap diedit di CapCut atau dibagikan ke status WhatsApp.',
            'fb_h': '🌐 Facebook Watch & Reels',
            'fb_d': 'Unduh klip dari beranda, grup publik, dan Facebook Watch dalam format MP4 H.264 standar untuk pemutaran lancar di semua perangkat.'
        },
        'guide5': {
            'title': 'Panduan Perangkat: Cara Menyimpan di Android, iPhone (iOS) & PC',
            'lead': 'Langkah penyimpanan berbeda di setiap sistem operasi. Ikuti panduan praktis berikut:',
            'and_h': '🤖 Ponsel Android (Samsung, Xiaomi, Oppo, Vivo, dll.)',
            'and_d': 'Tempel tautan di Chrome dan ketuk Unduh. File akan langsung tersimpan di folder Unduhan dan muncul di Galeri atau Google Foto.',
            'ios_h': '🍏 iPhone & iPad (Trik Rahasia Safari)',
            'ios_d': 'Di Safari, ketuk Unduh. Ketuk tanda panah biru unduhan di bilah URL -> buka video -> ketuk ikon Bagikan di kiri bawah -> pilih "Simpan Video". Video langsung masuk ke Foto / Rol Kamera!',
            'pc_h': '💻 Komputer Windows & Mac',
            'pc_d': 'Klik Unduh di Chrome, Edge, atau Safari. File akan langsung tersimpan di folder Downloads, kompatibel dengan VLC dan Windows Media Player.'
        },
        'faqs': [
            ('1. Bagaimana cara mengunduh video YouTube di ponsel?', 'Buka YouTube, klik Bagikan pada video, lalu salin tautan. Tempelkan di TheBhom, klik Analisis URL, pilih 1080p atau 720p, lalu klik Unduh untuk menyimpan ke ponsel.'),
            ('2. Bisakah mengunduh YouTube Shorts tanpa aplikasi tambahan?', 'Tentu saja! Tidak perlu aplikasi. Cukup salin tautan Shorts, tempel di TheBhom, dan unduh video vertikal 9:16 dalam satu klik.'),
            ('3. Bagaimana cara mengunduh Reels Instagram agar audionya tidak bisu?', 'TheBhom menggabungkan video 1080p dengan trek audio stereo AAC asli sehingga suara dan musiknya tidak akan pernah bisu.'),
            ('4. Di mana video unduhan tersimpan pada iPhone?', 'Di Safari, ketuk panah unduhan biru, buka video, ketuk ikon Bagikan di kiri bawah, lalu pilih "Simpan Video" untuk memindahkannya ke Rol Kamera.'),
            ('5. Apakah video TikTok diunduh tanpa tanda air (watermark)?', 'Ya! Sistem TheBhom mengambil video langsung dari sumber utama, sehingga video MP4 yang Anda peroleh benar-benar bersih tanpa logo TikTok.'),
            ('6. Bisakah mengambil lagu atau musik MP3 dari sebuah video?', 'Tentu bisa. Tempelkan URL video ke TheBhom, lalu pada daftar format pilih "MP3 Audio" untuk mengunduh trek suara 320kbps.'),
            ('7. Apakah harus login atau membayar untuk menggunakan TheBhom?', 'Tidak! TheBhom 100% gratis digunakan selamanya tanpa langganan, tanpa daftar akun, dan tanpa batas harian.'),
            ('8. Apakah video MP4 yang diunduh bisa diputar di WhatsApp dan aplikasi edit video?', 'Ya. Semua video menggunakan format standar H.264 MP4 dan audio AAC yang lancar diputar di WhatsApp, CapCut, Premiere Pro, dan VLC.')
        ],
        'nav_deals': 'Promo',
        'nav_downloader': 'Pengunduh',
        'nav_guides': 'Panduan',
        'disclaimer': '⚠️ Penafian: TheBhom adalah alat utilitas media pribadi dan tidak menyimpan video berhak cipta di server kami. Hanya untuk penggunaan arsip pribadi dan wajar.'
    }
}


def build_page_html(lang_key):
    cfg = LANGUAGES[lang_key]

    # Build Language Dropdown Options
    lang_options = []
    for lk, lcfg in LANGUAGES.items():
        val = lcfg['canonical'].replace('https://www.thebhom.in', '')
        sel = ' selected' if lk == lang_key else ''
        lang_options.append(f'<option value="{val}"{sel}>{lcfg["lang_name"]}</option>')
    lang_options_html = "\n            ".join(lang_options)

    # Build FAQs HTML
    faq_items = []
    faq_schema_entities = []
    for q, a in cfg['faqs']:
        faq_items.append(f'''          <div class="faq-item">
            <div class="faq-q">{q}</div>
            <div class="faq-a">{a}</div>
          </div>''')
        faq_schema_entities.append(f'''          {{
            "@type": "Question",
            "name": {json.dumps(q)},
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": {json.dumps(a)}
            }}
          }}''')
    faqs_html = "\n".join(faq_items)
    faq_schema_json = ",\n".join(faq_schema_entities)

    # Hreflang Tags (Identical across all 5 pages)
    hreflang_tags = """  <link rel="alternate" hreflang="x-default" href="https://www.thebhom.in/downloader/">
  <link rel="alternate" hreflang="en" href="https://www.thebhom.in/downloader/">
  <link rel="alternate" hreflang="hi" href="https://www.thebhom.in/downloader/hi/">
  <link rel="alternate" hreflang="es" href="https://www.thebhom.in/downloader/es/">
  <link rel="alternate" hreflang="pt" href="https://www.thebhom.in/downloader/pt/">
  <link rel="alternate" hreflang="id" href="https://www.thebhom.in/downloader/id/">"""

    html = f"""<!DOCTYPE html>
<html lang="{cfg['html_lang']}">
<head>
  <script>(function(){{try{{const t=localStorage.getItem('thebhom_theme')||'light';document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
  <meta name="google-adsense-account" content="ca-pub-4674566886677472">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4674566886677472" crossorigin="anonymous"></script>
  <meta name="google-site-verification" content="googlec324d892b7f2bbf5"/>
  <meta name="p:domain_verify" content="027b813eb55f730989b6236aea44ed88"/>

  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-K2B22XSW');</script>
  <!-- End Google Tag Manager -->

  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GHVNZWFVQV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-GHVNZWFVQV');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['meta_desc']}">
  <meta name="keywords" content="{cfg['keywords']}">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['meta_desc']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{cfg['canonical']}">
  <meta property="og:image" content="https://www.thebhom.in/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{cfg['og_locale']}">
  <meta property="og:site_name" content="TheBhom">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{cfg['title']}">
  <meta name="twitter:description" content="{cfg['meta_desc']}">
  <meta name="twitter:image" content="https://www.thebhom.in/og-image.png">
  <link rel="stylesheet" href="/shared.css?v=20261024_v1">
  <link rel="canonical" href="{cfg['canonical']}">
{hreflang_tags}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{cfg['schema_app_name']}",
    "operatingSystem": "Windows, macOS, Android, iOS, Linux",
    "applicationCategory": "UtilitiesApplication",
    "offers": {{
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    }}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebApplication",
        "name": "{cfg['schema_app_name']}",
        "url": "{cfg['canonical']}",
        "applicationCategory": "MultimediaApplication",
        "operatingSystem": "All",
        "description": "{cfg['schema_app_desc']}",
        "inLanguage": "{cfg['html_lang']}",
        "offers": {{
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "USD"
        }}
      }},
      {{
        "@type": "HowTo",
        "name": "{cfg['guide1']['title']}",
        "description": "{cfg['guide1']['lead'][:180]}...",
        "step": [
          {{
            "@type": "HowToStep",
            "name": "{cfg['guide1']['s1_h']}",
            "text": "{cfg['guide1']['s1_d']}"
          }},
          {{
            "@type": "HowToStep",
            "name": "{cfg['guide1']['s2_h']}",
            "text": "{cfg['guide1']['s2_d']}"
          }},
          {{
            "@type": "HowToStep",
            "name": "{cfg['guide1']['s3_h']}",
            "text": "{cfg['guide1']['s3_d']}"
          }}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
{faq_schema_json}
        ]
      }}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root, [data-theme="light"] {{
      --dl-bg: #f5f6f8;
      --dl-card: #ffffff;
      --dl-border: #e2e8f0;
      --dl-text: #111827;
      --dl-muted: #64748b;
      --dl-accent: #e5322d;
      --dl-accent-hover: #cb201b;
      --dl-accent-light: #fff1f0;
      --dl-input-bg: #ffffff;
      --dl-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    [data-theme="navy"] {{
      --dl-bg: #0b132b; --dl-card: rgba(20,32,66,0.95); --dl-border: rgba(56,189,248,0.22);
      --dl-text: #f1f5f9; --dl-muted: #94a3b8; --dl-accent: #38bdf8; --dl-accent-hover: #0ea5e9;
      --dl-accent-light: rgba(56,189,248,0.12); --dl-input-bg: rgba(11,19,43,0.9); --dl-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}
    [data-theme="purple"] {{
      --dl-bg: #0f0a1c; --dl-card: rgba(27,18,49,0.95); --dl-border: rgba(168,85,247,0.28);
      --dl-text: #f8fafc; --dl-muted: #c4b5fd; --dl-accent: #a855f7; --dl-accent-hover: #9333ea;
      --dl-accent-light: rgba(168,85,247,0.12); --dl-input-bg: rgba(15,10,28,0.9); --dl-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }}
    [data-theme="dark"] {{
      --dl-bg: #101216; --dl-card: #1c1f26; --dl-border: rgba(255,255,255,0.1);
      --dl-text: #f8fafc; --dl-muted: #9ca3af; --dl-accent: #e5322d; --dl-accent-hover: #cb201b;
      --dl-accent-light: rgba(229,50,45,0.12); --dl-input-bg: #14171e; --dl-shadow: 0 8px 32px rgba(0,0,0,0.6);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--dl-bg);
      color: var(--dl-text);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background 0.3s ease, color 0.3s ease;
    }}
    .container {{
      max-width: 1060px;
      margin: 0 auto;
      padding: 30px 20px 80px;
      width: 100%;
      flex-grow: 1;
    }}
    .header {{
      text-align: center;
      margin-bottom: 28px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--dl-accent-light);
      color: var(--dl-accent);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 14px;
      border: 1px solid rgba(229, 50, 45, 0.2);
    }}
    h1 {{
      font-size: clamp(26px, 4.2vw, 42px);
      font-weight: 800;
      letter-spacing: -0.8px;
      line-height: 1.25;
      margin-bottom: 12px;
      color: var(--dl-text);
    }}
    .subtitle {{
      font-size: 15.5px;
      color: var(--dl-muted);
      max-width: 720px;
      margin: 0 auto 20px;
      line-height: 1.6;
    }}
    .supported-platforms {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 24px;
    }}
    .plat-tag {{
      background: var(--dl-card);
      border: 1px solid var(--dl-border);
      padding: 4px 12px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--dl-muted);
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .tool-switcher-nav {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 8px;
      margin: 0 auto 24px;
      max-width: 900px;
    }}
    .tool-pill {{
      background: var(--dl-card);
      border: 1.5px solid var(--dl-border);
      color: var(--dl-text);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }}
    .tool-pill:hover {{
      border-color: var(--dl-accent);
      color: var(--dl-accent);
      transform: translateY(-1px);
    }}
    .tool-pill.active {{
      background: var(--dl-accent);
      border-color: var(--dl-accent);
      color: #ffffff;
      box-shadow: 0 3px 10px rgba(229, 50, 45, 0.3);
    }}
    .search-card {{
      background: var(--dl-card);
      border: 1.5px solid var(--dl-border);
      border-radius: 20px;
      padding: 18px 20px;
      box-shadow: var(--dl-shadow);
      margin-bottom: 28px;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .search-card:focus-within {{
      border-color: var(--dl-accent);
      box-shadow: 0 6px 24px rgba(229, 50, 45, 0.15);
    }}
    .input-group {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    @media(max-width: 680px) {{
      .input-group {{ flex-direction: column; align-items: stretch; }}
    }}
    .input-field-wrap {{
      position: relative;
      flex-grow: 1;
      display: flex;
      align-items: center;
    }}
    .url-input {{
      width: 100%;
      background: var(--dl-input-bg);
      border: 1.5px solid var(--dl-border);
      border-radius: 12px;
      padding: 14px 85px 14px 16px;
      font-size: 15px;
      color: var(--dl-text);
      outline: none;
      font-family: inherit;
      transition: border-color 0.2s;
    }}
    .url-input:focus {{ border-color: var(--dl-accent); }}
    .btn-paste-clipboard {{
      position: absolute;
      right: 8px;
      background: var(--dl-card);
      border: 1px solid var(--dl-border);
      color: var(--dl-muted);
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s ease;
    }}
    .btn-paste-clipboard:hover {{
      color: var(--dl-accent);
      border-color: var(--dl-accent);
    }}
    .btn-clear-input {{
      position: absolute;
      right: 76px;
      background: transparent;
      border: none;
      color: var(--dl-muted);
      cursor: pointer;
      padding: 4px;
      display: inline-flex;
      align-items: center;
    }}
    .btn-parse {{
      background: var(--dl-accent);
      color: #fff;
      border: none;
      border-radius: 12px;
      padding: 14px 28px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(229, 50, 45, 0.25);
      flex-shrink: 0;
    }}
    .btn-parse:hover {{
      background: var(--dl-accent-hover);
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(229, 50, 45, 0.35);
    }}
    .btn-parse:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; box-shadow: none; }}
    .result-card {{
      display: none;
      background: var(--dl-card);
      border: 1.5px solid var(--dl-border);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: var(--dl-shadow);
      animation: fadeIn 0.25s ease forwards;
    }}
    @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
    .result-header-clean {{
      padding: 20px 24px 16px;
      border-bottom: 1px solid var(--dl-border);
      display: flex; flex-direction: column; gap: 8px;
    }}
    .result-platform-row {{
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    }}
    .platform-pill {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 4px 12px; background: var(--dl-accent-light);
      border: 1px solid rgba(229, 50, 45, 0.3); border-radius: 9999px;
      font-size: 12px; font-weight: 800; color: var(--dl-accent);
    }}
    .info-title {{
      font-size: 18px; font-weight: 800; line-height: 1.4; color: var(--dl-text);
      word-break: break-word;
    }}
    .info-meta-row {{
      display: flex; gap: 10px; font-size: 13px; color: var(--dl-muted); align-items: center; flex-wrap: wrap;
    }}
    .engine-pill {{
      background: rgba(16,185,129,0.12); color: #16a34a; border: 1px solid rgba(16,185,129,0.3);
      padding: 2px 9px; border-radius: 9999px; font-weight: 700; font-size: 11px;
    }}
    .duration-pill {{
      font-weight: 700; font-family: monospace; background: var(--dl-bg);
      padding: 2px 8px; border-radius: 6px; border: 1px solid var(--dl-border); color: var(--dl-text);
    }}
    .player-stage-wrap {{
      width: 100%;
      background: #000;
      position: relative;
      border-bottom: 1px solid var(--dl-border);
    }}
    .stage-thumbnail {{
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      max-height: 420px;
      cursor: pointer;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0b0f19;
    }}
    .stage-thumb-img {{
      width: 100%; height: 100%; object-fit: cover;
      transition: transform 0.3s ease, filter 0.3s ease;
    }}
    .stage-thumbnail:hover .stage-thumb-img {{
      transform: scale(1.02);
      filter: brightness(0.85);
    }}
    .stage-play-overlay {{
      position: absolute;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 8px;
      pointer-events: none;
    }}
    .yt-play-btn {{
      width: 64px; height: 64px; border-radius: 50%;
      background: var(--dl-accent); color: #fff;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 20px rgba(229,50,45,0.5);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .stage-thumbnail:hover .yt-play-btn {{
      transform: scale(1.1);
      box-shadow: 0 6px 28px rgba(229,50,45,0.7);
    }}
    .yt-play-text {{
      color: #fff; font-size: 14px; font-weight: 800;
      text-shadow: 0 2px 8px rgba(0,0,0,0.8); letter-spacing: 0.3px;
    }}
    .yt-play-sub {{
      color: rgba(255,255,255,0.8); font-size: 11.5px; font-weight: 600;
      text-shadow: 0 1px 4px rgba(0,0,0,0.9);
    }}
    .stage-active-player video {{
      width: 100%; aspect-ratio: 16/9; max-height: 460px;
      background: #000; display: block; outline: none;
    }}
    .player-ctrl-bar {{
      padding: 10px 18px; background: rgba(15,23,42,0.95);
      display: flex; align-items: center; justify-content: space-between;
      color: #fff; font-size: 12.5px; flex-wrap: wrap; gap: 8px;
    }}
    .player-now-playing {{
      display: flex; align-items: center; gap: 8px; font-weight: 700;
    }}
    .live-pulse {{
      width: 8px; height: 8px; border-radius: 50%;
      background: #22c55e; box-shadow: 0 0 8px #22c55e;
      animation: pulseGreen 1.5s infinite;
    }}
    @keyframes pulseGreen {{
      0% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .player-action-btns {{
      display: flex; align-items: center; gap: 8px;
    }}
    .player-btn-secondary, .player-btn-close {{
      background: rgba(255,255,255,0.12); color: #fff;
      border: 1px solid rgba(255,255,255,0.2); border-radius: 6px;
      padding: 4px 10px; font-size: 11.5px; font-weight: 700;
      cursor: pointer; transition: background 0.2s;
    }}
    .player-btn-secondary:hover {{ background: rgba(255,255,255,0.22); }}
    .player-btn-close:hover {{ background: #dc2626; border-color: #dc2626; }}
    .stage-active-audio {{
      padding: 30px 24px; text-align: center;
      background: linear-gradient(135deg, #1e1b4b, #0f172a);
      color: #fff;
    }}
    .audio-wave-ic {{ font-size: 38px; margin-bottom: 8px; }}
    .audio-title-clean {{ font-size: 15px; font-weight: 700; margin-bottom: 4px; color: #f8fafc; }}
    .audio-badge-clean {{ font-size: 12px; color: #a5b4fc; font-weight: 600; margin-bottom: 12px; }}
    .result-body {{
      padding: 24px; display: flex; flex-direction: column; gap: 20px;
    }}
    .format-section-title {{
      display: flex; align-items: center; justify-content: space-between;
      font-size: 15px; font-weight: 800; color: var(--dl-text);
      margin-bottom: 4px; flex-wrap: wrap; gap: 6px;
    }}
    .format-subtext {{ font-size: 12.5px; color: var(--dl-muted); font-weight: 500; }}
    .format-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 12px;
    }}
    .fmt-card {{
      background: var(--dl-card); border: 1.5px solid var(--dl-border);
      border-radius: 12px; padding: 14px 16px; display: flex;
      flex-direction: column; gap: 10px; transition: all 0.2s ease;
      cursor: pointer; position: relative;
    }}
    .fmt-card:hover {{
      border-color: var(--dl-accent);
      box-shadow: 0 4px 14px rgba(229, 50, 45, 0.12);
      transform: translateY(-2px);
    }}
    .fmt-card.selected {{
      border-color: var(--dl-accent);
      background: var(--dl-accent-light);
    }}
    .fmt-top {{
      display: flex; justify-content: space-between; align-items: center;
    }}
    .fmt-badge {{
      background: var(--dl-accent); color: #fff;
      font-size: 11px; font-weight: 800; padding: 2px 7px;
      border-radius: 4px; letter-spacing: 0.3px;
    }}
    .fmt-badge.audio-badge {{ background: #8b5cf6; }}
    .fmt-size {{ font-size: 12px; color: var(--dl-muted); font-weight: 600; }}
    .fmt-quality {{ font-size: 15px; font-weight: 800; color: var(--dl-text); }}
    .fmt-actions {{
      display: flex; gap: 8px; margin-top: auto;
    }}
    .fmt-btn-preview, .fmt-btn-download {{
      flex: 1; padding: 7px 0; border-radius: 6px;
      font-size: 12px; font-weight: 700; text-align: center;
      cursor: pointer; border: none; transition: all 0.15s ease;
      text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px;
    }}
    .fmt-btn-preview {{
      background: var(--dl-card); border: 1px solid var(--dl-border); color: var(--dl-text);
    }}
    .fmt-btn-preview:hover {{ background: var(--dl-bg); border-color: var(--dl-accent); color: var(--dl-accent); }}
    .fmt-btn-download {{
      background: var(--dl-accent); color: #fff;
    }}
    .fmt-btn-download:hover {{ background: var(--dl-accent-hover); }}
    .trimmer-box {{
      background: var(--dl-bg); border: 1px dashed var(--dl-border);
      border-radius: 12px; padding: 14px 18px;
    }}
    .trimmer-header {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 12px; flex-wrap: wrap;
    }}
    .trimmer-inputs {{
      display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap;
    }}
    .trim-field {{ display: flex; align-items: center; gap: 8px; }}
    .trim-input {{
      width: 80px; padding: 6px 8px; border-radius: 6px;
      border: 1px solid var(--dl-border); background: var(--dl-card);
      color: var(--dl-text); font-family: monospace; font-size: 13px; font-weight: 700;
    }}
    .download-actions {{
      display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 6px;
    }}
    .btn-download-start {{
      background: var(--dl-accent); color: #fff; border: none;
      border-radius: 14px; padding: 16px 36px; font-size: 16px;
      font-weight: 800; cursor: pointer; transition: all 0.2s ease;
      box-shadow: 0 4px 18px rgba(229, 50, 45, 0.35); width: 100%; max-width: 440px;
      display: flex; align-items: center; justify-content: center; gap: 8px;
    }}
    .btn-download-start:hover {{
      background: var(--dl-accent-hover); transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(229, 50, 45, 0.45);
    }}
    .btn-download-start:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; box-shadow: none; }}
    .status-msg {{ font-size: 13.5px; font-weight: 600; color: var(--dl-accent); min-height: 20px; }}
    .download-success-banner {{
      display: none; background: #ecfdf5; border: 1.5px solid #a7f3d0;
      border-radius: 12px; padding: 14px 18px; align-items: center;
      justify-content: space-between; gap: 14px; flex-wrap: wrap;
    }}
    .seo-hub-wrap {{
      margin-top: 40px; display: flex; flex-direction: column; gap: 24px;
    }}
    .seo-guide-nav {{
      display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
      margin-bottom: 8px;
    }}
    .seo-guide-pill {{
      background: var(--dl-card); border: 1px solid var(--dl-border);
      color: var(--dl-text); text-decoration: none; padding: 6px 14px;
      border-radius: 9999px; font-size: 13px; font-weight: 700;
      transition: all 0.2s;
    }}
    .seo-guide-pill:hover {{
      border-color: var(--dl-accent); color: var(--dl-accent); transform: translateY(-1px);
    }}
    .seo-card {{
      background: var(--dl-card); border: 1.5px solid var(--dl-border);
      border-radius: 18px; padding: 28px 24px; box-shadow: var(--dl-shadow);
    }}
    .seo-card-title {{
      display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
    }}
    .seo-card-title h2 {{
      font-size: 20px; font-weight: 800; line-height: 1.35; color: var(--dl-text); margin: 0;
    }}
    .seo-lead-text {{
      font-size: 14.5px; color: var(--dl-muted); line-height: 1.65; margin-bottom: 20px;
    }}
    .seo-steps-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px; margin-bottom: 18px;
    }}
    .seo-step-item {{
      background: var(--dl-bg); border: 1px solid var(--dl-border);
      border-radius: 14px; padding: 18px; position: relative;
    }}
    .seo-step-num {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 28px; height: 28px; border-radius: 50%; background: var(--dl-accent);
      color: #fff; font-weight: 800; font-size: 13px; margin-bottom: 10px;
    }}
    .seo-step-head {{
      font-size: 14.5px; font-weight: 800; color: var(--dl-text); margin-bottom: 6px;
    }}
    .seo-step-desc {{
      font-size: 13px; color: var(--dl-muted); line-height: 1.55;
    }}
    .seo-pro-tip {{
      background: var(--dl-accent-light); border-left: 4px solid var(--dl-accent);
      border-radius: 8px; padding: 12px 16px; font-size: 13.5px;
      color: var(--dl-text); display: flex; gap: 10px; align-items: flex-start;
      line-height: 1.5;
    }}
    .seo-platform-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px; margin-top: 14px;
    }}
    .seo-platform-card {{
      background: var(--dl-bg); border: 1px solid var(--dl-border);
      border-radius: 14px; padding: 18px;
    }}
    .seo-platform-card h3 {{
      font-size: 16px; font-weight: 800; margin-bottom: 8px; color: var(--dl-text);
    }}
    .faq-list {{
      display: flex; flex-direction: column; gap: 12px; margin-top: 14px;
    }}
    .faq-item {{
      background: var(--dl-bg); border: 1px solid var(--dl-border);
      border-radius: 12px; padding: 16px 18px;
    }}
    .faq-q {{
      font-size: 15px; font-weight: 800; color: var(--dl-text); margin-bottom: 6px;
    }}
    .faq-a {{
      font-size: 13.5px; color: var(--dl-muted); line-height: 1.6;
    }}
    .thebhom-lang-select {{
      background: var(--dl-card); color: var(--dl-text);
      border: 1.5px solid var(--dl-border); padding: 5px 10px;
      border-radius: 10px; font-size: 12.5px; font-weight: 700;
      cursor: pointer; outline: none; font-family: inherit;
    }}
  </style>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K2B22XSW"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <!-- TOP APP NAVIGATION -->
  <div class="scroll-prog" id="sp"></div>
  <header class="hdr">
    <a href="/" class="logo" title="TheBhom — Home">
      <div class="logo-box" style="background:linear-gradient(135deg, #e11d48, #be123c);border-radius:11px;color:#fff;font-weight:900;">TB</div>
      <span class="logo-txt">The<span class="brand-accent" style="color:#e11d48;">Bhom</span></span>
    </a>
    <nav class="hdr-nav-container">
      <ul class="hdr-nav">
        <li><a href="/deals/" class="hdr-nav-link" title="TheBhom Deals"><span class="hdr-nav-ic" style="color:#f59e0b;"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><circle cx="7" cy="7" r="1.5"/></svg></span><span class="hdr-nav-txt" style="color:#f59e0b;font-weight:700;">{cfg['nav_deals']}</span></a></li>
        <li><a href="/downloader/" class="hdr-nav-link active" title="Universal Video Downloader"><span class="hdr-nav-ic" style="color:#0891b2;"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></span><span class="hdr-nav-txt" style="color:#0891b2;font-weight:700;">{cfg['nav_downloader']}</span></a></li>
        <li><a href="/guides/" class="hdr-nav-link" title="TheBhom Guides & Reviews"><span class="hdr-nav-ic" style="color:#10b981;"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg></span><span class="hdr-nav-txt" style="color:#10b981;font-weight:700;">{cfg['nav_guides']}</span></a></li>
      </ul>
    </nav>
    <div class="hdr-right">
      <div class="thebhom-lang-container" style="display:inline-flex;align-items:center;margin-right:6px;">
        <select class="thebhom-lang-select" onchange="navigateDownloaderLang(this.value)" aria-label="Select Language">
          {lang_options_html}
        </select>
      </div>
      <div class="hdr-search-pill" onclick="openSpotlight()" role="button" tabindex="0" title="Search (⌘K)">
        <svg class="hdr-search-ic" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <span class="hdr-search-txt">Search...</span>
        <kbd class="hdr-search-kbd">⌘K</kbd>
      </div>
      <button class="hdr-theme-btn" id="hdrThemeBtn" onclick="quickToggleTheme()" title="Toggle Theme" aria-label="Toggle Theme">
        <svg class="theme-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>
      </button>
      <button class="ham" id="hamBtn" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <nav class="mob-nav" id="mobNav">
    <div class="mob-theme-row">
      <span style="font-size:0.8rem;font-weight:700;color:var(--text2);margin-right:6px;">🎨 Theme:</span>
      <button class="mob-theme-pill" data-theme="light" onclick="setAppTheme('light')">☀️ Light</button>
      <button class="mob-theme-pill" data-theme="navy" onclick="setAppTheme('navy')">🌊 Navy</button>
      <button class="mob-theme-pill" data-theme="purple" onclick="setAppTheme('purple')">🔮 Purple</button>
      <button class="mob-theme-pill" data-theme="dark" onclick="setAppTheme('dark')">🌙 Dark</button>
    </div>
    <div style="padding:10px 0;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--dl-border);">
      <span style="font-size:0.8rem;font-weight:700;color:var(--text2);">🌐 Language:</span>
      <select class="thebhom-lang-select" onchange="navigateDownloaderLang(this.value)" aria-label="Select Mobile Language">
        {lang_options_html}
      </select>
    </div>
    <a href="/">🏠 Home</a>
    <a href="/deals/" style="color:#f59e0b;font-weight:700;">🔥 {cfg['nav_deals']}</a>
    <a href="/downloader/" class="active" style="color:#0891b2;font-weight:700;">⚡ {cfg['nav_downloader']}</a>
    <a href="/guides/" style="color:#10b981;font-weight:700;">📖 {cfg['nav_guides']}</a>
    <a href="/about">ℹ️ About Us</a>
    <a href="/contact">📞 Contact</a>
    <a href="#" onclick="openSpotlight();return false;" style="color:#2563eb;font-weight:700;">🔍 Search (Cmd+K)</a>
  </nav>

  <div class="container">

    <header class="header">
      <div class="badge">{cfg['badge']}</div>
      <h1>{cfg['hero_title']}</h1>
      <p class="subtitle">{cfg['hero_subtitle']}</p>

      <div class="supported-platforms">
        <span class="plat-tag">YouTube & Shorts</span>
        <span class="plat-tag">Instagram Reels</span>
        <span class="plat-tag">TikTok</span>
        <span class="plat-tag">Facebook</span>
        <span class="plat-tag">Twitter / X</span>
        <span class="plat-tag">Pinterest</span>
        <span class="plat-tag">Reddit</span>
      </div>
    </header>

    <!-- Dedicated Sub-Tool Switcher Pills -->
    <nav class="tool-switcher-nav" aria-label="Specialized Platform Downloaders">
      <a href="/downloader/" class="tool-pill active">⚡ All-in-One</a>
      <a href="/downloader/video-to-mp3-converter.html" class="tool-pill" style="border-color:#e5322d;background:var(--dl-accent-light);color:var(--dl-accent);font-weight:800;">🎧 Video to MP3</a>
      <a href="/downloader/youtube-video-downloader.html" class="tool-pill">▶ YouTube Video</a>
      <a href="/downloader/youtube-shorts-downloader.html" class="tool-pill">⚡ YouTube Shorts</a>
      <a href="/downloader/youtube-song-downloader.html" class="tool-pill">🎵 YouTube Song / MP3</a>
      <a href="/downloader/instagram-reels-downloader.html" class="tool-pill">📸 Instagram Reels</a>
      <a href="/downloader/instagram-story-downloader.html" class="tool-pill">📖 Instagram Story</a>
      <a href="/downloader/tiktok-video-downloader.html" class="tool-pill">🎵 TikTok (No Watermark)</a>
      <a href="/downloader/facebook-video-downloader.html" class="tool-pill">🌐 Facebook</a>
      <a href="/downloader/twitter-video-downloader.html" class="tool-pill">🐦 Twitter / X</a>
      <a href="/downloader/pinterest-video-downloader.html" class="tool-pill">📌 Pinterest</a>
      <a href="/downloader/reddit-video-downloader.html" class="tool-pill">👾 Reddit</a>
    </nav>

    <!-- URL Input Card -->
    <div class="search-card">
      <div class="input-group">
        <div class="input-field-wrap">
          <input type="text" id="videoUrl" class="url-input" placeholder="{cfg['input_placeholder']}" oninput="handleInputChange()" autocomplete="off" />
          <button type="button" id="clearBtn" class="btn-clear-input" onclick="clearUrlInput()" style="display:none;" title="Clear input">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
          <button type="button" id="pasteBtn" class="btn-paste-clipboard" onclick="handleClipboardPaste()" title="Paste URL from Clipboard">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>{cfg['paste_btn']}</span>
          </button>
        </div>
        <button id="parseBtn" class="btn-parse" onclick="analyzeVideo()">
          <span>{cfg['analyze_btn']}</span>
        </button>
      </div>
    </div>

    <!-- Result / Download Card with Streaming Player -->
    <div id="resultCard" class="result-card">
      
      <!-- Video Header -->
      <div class="result-header-clean">
        <div class="result-platform-row">
          <div class="platform-pill" id="resPlatformBadge">
            <span id="resPlatformIcon">⚡</span>
            <span id="resPlatformName">Online Video</span>
          </div>
          <div class="info-meta-row">
            <span id="resAuthor">Creator</span>
            <span>•</span>
            <span id="resDuration" class="duration-pill">00:00</span>
            <span>•</span>
            <span id="resEngine" class="engine-pill">⚡ Fast Cloud Stream</span>
          </div>
        </div>
        <h2 id="resTitle" class="info-title">Video Title</h2>
      </div>

      <!-- INLINE STREAMING PLAYER STAGE -->
      <div class="player-stage-wrap" id="playerStageWrap">
        <!-- 1. Thumbnail View with Play Button -->
        <div class="stage-thumbnail" id="stageThumbnail" onclick="startInstantPlayback()" title="{cfg['watch_online_sub']}">
          <img id="resThumb" class="stage-thumb-img" src="" alt="Thumbnail" />
          <div class="stage-play-overlay">
            <div class="yt-play-btn">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
            </div>
            <div class="yt-play-text">{cfg['watch_online_btn']}</div>
            <div class="yt-play-sub">{cfg['watch_online_sub']}</div>
          </div>
        </div>

        <!-- 2. Active Video Player -->
        <div class="stage-active-player" id="stageActivePlayer" style="display: none;">
          <video id="inlineVideoPlayer" controls playsinline preload="metadata"></video>
          <div class="player-ctrl-bar">
            <div class="player-now-playing">
              <span class="live-pulse"></span>
              <span id="playerNowPlayingLabel">{cfg['streaming_label']}</span>
            </div>
            <div class="player-action-btns">
              <button class="player-btn-secondary" onclick="openActiveInNewTab()" title="Open media stream in new tab">{cfg['new_tab_btn']}</button>
              <button class="player-btn-close" onclick="closeInlinePlayer()" title="Close player and return to thumbnail">{cfg['close_player_btn']}</button>
            </div>
          </div>
        </div>

        <!-- 3. Active Audio MP3 Player -->
        <div class="stage-active-audio" id="stageActiveAudio" style="display: none;">
          <div class="audio-wave-ic">🎵</div>
          <div id="inlineAudioTitle" class="audio-title-clean">{cfg['audio_track_label']}</div>
          <div class="audio-badge-clean">{cfg['audio_fidelity_label']}</div>
          <audio id="inlineAudioPlayer" controls style="width: 100%; max-width: 520px; margin-top: 8px;"></audio>
          <button class="player-btn-close" onclick="closeInlinePlayer()" style="margin-top: 8px;">{cfg['close_player_btn']}</button>
        </div>

        <!-- 4. Active Embedded Video Player -->
        <div class="stage-active-player" id="stageActiveEmbed" style="display: none; position: relative; width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden;">
          <iframe id="inlineEmbedFrame" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border: 0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
          <div class="player-ctrl-bar" style="position: absolute; bottom: 0; left: 0; right: 0; z-index: 10; background: linear-gradient(transparent, rgba(0,0,0,0.85));">
            <div class="player-now-playing">
              <span class="live-pulse"></span>
              <span id="playerEmbedLabel">Live HD Preview</span>
            </div>
            <div class="player-action-btns">
              <button class="player-btn-close" onclick="closeInlinePlayer()" title="Close player and return to thumbnail">{cfg['close_player_btn']}</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Result Body: Format Cards -->
      <div class="result-body">
        <div>
          <div class="format-section-title">
            <span>{cfg['formats_title']}</span>
            <span class="format-subtext">{cfg['formats_sub']}</span>
          </div>
          <div id="formatsGrid" class="format-grid" style="margin-top: 12px;"></div>
        </div>

        <!-- Precision Trimmer -->
        <div class="trimmer-box">
          <div class="trimmer-header">
            <div>
              <strong style="color: var(--dl-text); font-size: 14px;">{cfg['trimmer_title']}</strong>
              <div style="font-size: 12px; color: var(--dl-muted);">{cfg['trimmer_sub']}</div>
            </div>
            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px;">
              <input type="checkbox" id="enableTrim" onchange="toggleTrimInputs()" />
              <span style="font-weight: 600;">{cfg['enable_trimmer']}</span>
            </label>
          </div>

          <div id="trimInputs" class="trimmer-inputs" style="display: none;">
            <div class="trim-field">
              <span style="font-size: 13px; color: var(--dl-muted);">{cfg['start_time']}</span>
              <input type="text" id="trimStart" class="trim-input" placeholder="00:05" value="00:00" />
            </div>
            <div class="trim-field">
              <span style="font-size: 13px; color: var(--dl-muted);">{cfg['end_time']}</span>
              <input type="text" id="trimEnd" class="trim-input" placeholder="00:15" value="00:10" />
            </div>
          </div>
        </div>

        <!-- Download Action -->
        <div class="download-actions">
          <span id="statusMsg" class="status-msg"></span>
          <button id="downloadBtn" class="btn-download-start" onclick="startDownload()">
            <span>{cfg['download_selected_btn']}</span>
          </button>
        </div>

        <!-- Success banner -->
        <div id="successBanner" class="download-success-banner">
          <div>
            <strong style="color: #16a34a;">{cfg['download_ready']}</strong>
            <div id="savedFilename" style="font-size: 13px; color: var(--dl-text); margin-top: 2px;"></div>
          </div>
          <a id="savedLink" href="#" download class="btn-parse" style="text-decoration: none; padding: 10px 20px;">
            {cfg['save_to_device']}
          </a>
        </div>

      </div>
    </div>

    <!-- AdSense Auto Display Unit -->
    <div class="ad-unit-wrapper auto-display" style="margin: 8px 0;">
      <span class="ad-label">Advertisement</span>
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-4674566886677472"
           data-ad-slot="5470514139"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({{}});
      </script>
    </div>

    <!-- In-Article Fluid Unit -->
    <div class="ad-unit-wrapper fluid-in-article">
      <span class="ad-label">Advertisement</span>
      <ins class="adsbygoogle"
           style="display:block; text-align:center;"
           data-ad-layout="in-article"
           data-ad-format="fluid"
           data-ad-client="ca-pub-4674566886677472"
           data-ad-slot="9101298657"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({{}});
      </script>
    </div>

    <!-- SEO Hub & Editorial Content in Native Language -->
    <div class="seo-hub-wrap">

      <!-- Quick Platform Jump Navigation -->
      <div class="seo-guide-nav">
        <a href="#guide-youtube" class="seo-guide-pill">{cfg['jump_nav']['yt']}</a>
        <a href="#guide-shorts" class="seo-guide-pill">{cfg['jump_nav']['shorts']}</a>
        <a href="#guide-reels" class="seo-guide-pill">{cfg['jump_nav']['reels']}</a>
        <a href="#guide-tiktok" class="seo-guide-pill">{cfg['jump_nav']['tiktok']}</a>
        <a href="#guide-facebook" class="seo-guide-pill">{cfg['jump_nav']['fb']}</a>
        <a href="#guide-devices" class="seo-guide-pill">{cfg['jump_nav']['devices']}</a>
        <a href="#guide-faq" class="seo-guide-pill">{cfg['jump_nav']['faqs']}</a>
      </div>

      <!-- Guide 1: YouTube Video Download -->
      <div class="seo-card" id="guide-youtube">
        <div class="seo-card-title">
          <span style="color:#ef4444;">▶️</span>
          <h2>{cfg['guide1']['title']}</h2>
        </div>
        <p class="seo-lead-text">{cfg['guide1']['lead']}</p>

        <div class="seo-steps-grid">
          <div class="seo-step-item">
            <div class="seo-step-num">1</div>
            <div class="seo-step-head">{cfg['guide1']['s1_h']}</div>
            <div class="seo-step-desc">{cfg['guide1']['s1_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">2</div>
            <div class="seo-step-head">{cfg['guide1']['s2_h']}</div>
            <div class="seo-step-desc">{cfg['guide1']['s2_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">3</div>
            <div class="seo-step-head">{cfg['guide1']['s3_h']}</div>
            <div class="seo-step-desc">{cfg['guide1']['s3_d']}</div>
          </div>
        </div>

        <div class="seo-pro-tip">
          <span>💡</span>
          <div>{cfg['guide1']['tip']}</div>
        </div>
      </div>

      <!-- Guide 2: YouTube Shorts -->
      <div class="seo-card" id="guide-shorts">
        <div class="seo-card-title">
          <span style="color:#dc2626;">⚡</span>
          <h2>{cfg['guide2']['title']}</h2>
        </div>
        <p class="seo-lead-text">{cfg['guide2']['lead']}</p>

        <div class="seo-steps-grid">
          <div class="seo-step-item">
            <div class="seo-step-num">1</div>
            <div class="seo-step-head">{cfg['guide2']['s1_h']}</div>
            <div class="seo-step-desc">{cfg['guide2']['s1_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">2</div>
            <div class="seo-step-head">{cfg['guide2']['s2_h']}</div>
            <div class="seo-step-desc">{cfg['guide2']['s2_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">3</div>
            <div class="seo-step-head">{cfg['guide2']['s3_h']}</div>
            <div class="seo-step-desc">{cfg['guide2']['s3_d']}</div>
          </div>
        </div>
      </div>

      <!-- Guide 3: Instagram Reels -->
      <div class="seo-card" id="guide-reels">
        <div class="seo-card-title">
          <span style="color:#e11d48;">📸</span>
          <h2>{cfg['guide3']['title']}</h2>
        </div>
        <p class="seo-lead-text">{cfg['guide3']['lead']}</p>

        <div class="seo-steps-grid">
          <div class="seo-step-item">
            <div class="seo-step-num">1</div>
            <div class="seo-step-head">{cfg['guide3']['s1_h']}</div>
            <div class="seo-step-desc">{cfg['guide3']['s1_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">2</div>
            <div class="seo-step-head">{cfg['guide3']['s2_h']}</div>
            <div class="seo-step-desc">{cfg['guide3']['s2_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-num">3</div>
            <div class="seo-step-head">{cfg['guide3']['s3_h']}</div>
            <div class="seo-step-desc">{cfg['guide3']['s3_d']}</div>
          </div>
        </div>

        <div class="seo-pro-tip">
          <span>🔒</span>
          <div>{cfg['guide3']['tip']}</div>
        </div>
      </div>

      <!-- Guide 4: TikTok & Facebook -->
      <div class="seo-card" id="guide-tiktok">
        <div class="seo-card-title">
          <span style="color:#0891b2;">🎵</span>
          <h2>{cfg['guide4']['title']}</h2>
        </div>
        <p class="seo-lead-text">{cfg['guide4']['lead']}</p>
        <div class="seo-platform-grid">
          <div class="seo-platform-card">
            <h3>{cfg['guide4']['tt_h']}</h3>
            <p style="font-size:13.5px;color:var(--dl-muted);line-height:1.5;">{cfg['guide4']['tt_d']}</p>
          </div>
          <div class="seo-platform-card" id="guide-facebook">
            <h3>{cfg['guide4']['fb_h']}</h3>
            <p style="font-size:13.5px;color:var(--dl-muted);line-height:1.5;">{cfg['guide4']['fb_d']}</p>
          </div>
        </div>
      </div>

      <!-- Guide 5: Devices -->
      <div class="seo-card" id="guide-devices">
        <div class="seo-card-title">
          <span style="color:#10b981;">📱</span>
          <h2>{cfg['guide5']['title']}</h2>
        </div>
        <p class="seo-lead-text">{cfg['guide5']['lead']}</p>

        <div class="seo-steps-grid">
          <div class="seo-step-item">
            <div class="seo-step-head" style="color:#10b981;">{cfg['guide5']['and_h']}</div>
            <div class="seo-step-desc">{cfg['guide5']['and_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-head" style="color:#0284c7;">{cfg['guide5']['ios_h']}</div>
            <div class="seo-step-desc">{cfg['guide5']['ios_d']}</div>
          </div>
          <div class="seo-step-item">
            <div class="seo-step-head" style="color:#8b5cf6;">{cfg['guide5']['pc_h']}</div>
            <div class="seo-step-desc">{cfg['guide5']['pc_d']}</div>
          </div>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="seo-card" id="guide-faq">
        <div class="seo-card-title">
          <span style="color:#f59e0b;">❓</span>
          <h2>Frequently Asked Questions</h2>
        </div>
        <div class="faq-list">
{faqs_html}
        </div>
      </div>

      <!-- Footer & Disclaimers -->
      <footer style="margin-top: 12px; padding: 28px 0 16px; border-top: 1px solid var(--dl-border); text-align: center;">
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 18px; margin-bottom: 16px; font-size: 14px;">
          <a href="/" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Home</a>
          <span style="color: var(--dl-border);">•</span>
          <a href="/deals/" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Deals</a>
          <span style="color: var(--dl-border);">•</span>
          <a href="/guides/" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Guides</a>
          <span style="color: var(--dl-border);">•</span>
          <a href="/privacy-policy" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Privacy Policy</a>
          <span style="color: var(--dl-border);">•</span>
          <a href="/terms" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Terms</a>
          <span style="color: var(--dl-border);">•</span>
          <a href="/disclaimer" style="color: var(--dl-muted); text-decoration: none; font-weight:600;">Disclaimer</a>
        </div>
        <!-- Semantic Crawlable Language Discovery Links -->
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; font-size: 13px; font-weight: 700;">
          <a href="/downloader/" style="color: var(--dl-muted); text-decoration: none; padding: 4px 10px; border-radius: 6px; background: var(--dl-bg); border: 1px solid var(--dl-border);">🇬🇧 English</a>
          <a href="/downloader/hi/" style="color: var(--dl-muted); text-decoration: none; padding: 4px 10px; border-radius: 6px; background: var(--dl-bg); border: 1px solid var(--dl-border);">🇮🇳 हिन्दी</a>
          <a href="/downloader/es/" style="color: var(--dl-muted); text-decoration: none; padding: 4px 10px; border-radius: 6px; background: var(--dl-bg); border: 1px solid var(--dl-border);">🇪🇸 Español</a>
          <a href="/downloader/pt/" style="color: var(--dl-muted); text-decoration: none; padding: 4px 10px; border-radius: 6px; background: var(--dl-bg); border: 1px solid var(--dl-border);">🇧🇷 Português</a>
          <a href="/downloader/id/" style="color: var(--dl-muted); text-decoration: none; padding: 4px 10px; border-radius: 6px; background: var(--dl-bg); border: 1px solid var(--dl-border);">🇮🇩 Bahasa Indonesia</a>
        </div>

        <!-- Official Social & Store Badges Strip -->
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 18px;">
          <a href="https://www.amazon.in/shop/bhom120704" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--dl-border); padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #fbbf24; text-decoration: none;">
            <span>📦</span> Amazon Storefront
          </a>
          <a href="https://cute-animals-pages.whop.site/" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--dl-border); padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #fb923c; text-decoration: none;">
            <span>🎨</span> Whop Coloring Books
          </a>
          <a href="https://in.pinterest.com/bhomvrat/" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--dl-border); padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #f87171; text-decoration: none;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 0 1 .083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.627-5.373-12-12-12z"/></svg>
            Pinterest
          </a>
          <a href="https://www.instagram.com/fashion_deals1207/" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--dl-border); padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #f472b6; text-decoration: none;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            Instagram
          </a>
          <a href="https://www.facebook.com/profile.php?id=61595491710213" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--dl-border); padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #60a5fa; text-decoration: none;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            Facebook
          </a>
        </div>
        <p style="font-size: 12px; color: var(--dl-muted); margin-bottom: 8px;">
          {cfg['disclaimer']}
        </p>
        <p style="font-size: 12px; color: var(--dl-muted);">
          © 2026 TheBhom Network (<a href="https://thebhom.in" style="color: var(--dl-accent); text-decoration: none; font-weight:700;">thebhom.in</a>). All rights reserved.
        </p>
      </footer>

    </div>

  </div>

  <script>
    function navigateDownloaderLang(targetUrl) {{
      const currentPath = window.location.pathname;
      const normalizedTarget = targetUrl.endsWith('/') ? targetUrl : targetUrl + '/';
      const normalizedCurrent = currentPath.endsWith('/') ? currentPath : currentPath + '/';
      if (normalizedTarget !== normalizedCurrent) {{
        const q = window.location.search || '';
        window.location.href = targetUrl + q;
      }}
    }}

    let currentData = null;
    let selectedQuality = "best";

    function formatSec(s) {{
      const m = Math.floor(s / 60);
      const sec = Math.floor(s % 60);
      return `${{String(m).padStart(2, '0')}}:${{String(sec).padStart(2, '0')}}`;
    }}

    function formatBytes(bytes) {{
      if (!bytes || bytes === 0) return 'Stream';
      const k = 1024;
      const dm = 1;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }}

    function toggleTrimInputs() {{
      const isEnabled = document.getElementById("enableTrim").checked;
      document.getElementById("trimInputs").style.display = isEnabled ? "flex" : "none";
    }}

    function getPlatformMeta(platform, url) {{
      const u = (url || "").toLowerCase();
      if (platform === "youtube" || u.includes("youtube.com") || u.includes("youtu.be")) {{
        return {{ name: "YouTube Video / Short", icon: "▶" }};
      }}
      if (platform === "instagram" || u.includes("instagram.com")) {{
        return {{ name: "Instagram Reel", icon: "📸" }};
      }}
      if (platform === "tiktok" || u.includes("tiktok.com")) {{
        return {{ name: "TikTok Video", icon: "🎵" }};
      }}
      if (platform === "facebook" || u.includes("facebook.com") || u.includes("fb.watch")) {{
        return {{ name: "Facebook Clip", icon: "📘" }};
      }}
      if (platform === "twitter" || u.includes("twitter.com") || u.includes("x.com")) {{
        return {{ name: "Twitter / X Video", icon: "🐦" }};
      }}
      if (platform === "pinterest" || u.includes("pinterest.com") || u.includes("pin.it")) {{
        return {{ name: "Pinterest Video", icon: "📌" }};
      }}
      if (platform === "reddit" || u.includes("reddit.com") || u.includes("redd.it")) {{
        return {{ name: "Reddit Video", icon: "👾" }};
      }}
      return {{ name: "Universal Stream", icon: "⚡" }};
    }}

    function getPlatformGatewayUrl(platform, rawUrl) {{
      const u = encodeURIComponent(rawUrl);
      if (platform === "youtube") return `https://www.y2mate.com/search/${{u}}`;
      if (platform === "instagram") return `https://snapinsta.app/`;
      if (platform === "tiktok") return `https://snaptik.app/`;
      if (platform === "facebook") return `https://fdownloader.net/`;
      if (platform === "twitter") return `https://twdown.net/`;
      if (platform === "pinterest") return `https://pinterestdownloader.com/`;
      if (platform === "reddit") return `https://rapidsave.com/`;
      return `https://savefrom.net/`;
    }}

    function parsePlatformDetails(rawUrl) {{
      const u = (rawUrl || "").trim();
      let platform = "general";
      let videoId = "";
      let title = "Online Video";
      let author = "Creator";
      let thumbnail = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe";
      let embedUrl = "";

      const ytMatch = u.match(/(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|shorts\/|live\/)([a-zA-Z0-9_-]{{11}})/);
      if (ytMatch) {{
        platform = "youtube";
        videoId = ytMatch[1];
        title = `YouTube Video (${{videoId}})`;
        author = "YouTube Creator";
        thumbnail = `https://i.ytimg.com/vi/${{videoId}}/hq720.jpg`;
        embedUrl = `https://www.youtube-nocookie.com/embed/${{videoId}}?autoplay=1`;
      }} else if (u.includes("instagram.com")) {{
        platform = "instagram";
        const igMatch = u.match(/(?:p|reel|tv)\/([a-zA-Z0-9_-]+)/);
        if (igMatch) videoId = igMatch[1];
        title = "Instagram Reel" + (videoId ? ` (${{videoId}})` : "");
        author = "Instagram Creator";
        thumbnail = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe";
      }} else if (u.includes("tiktok.com")) {{
        platform = "tiktok";
        title = "TikTok Video";
        author = "TikTok Creator";
      }} else if (u.includes("facebook.com") || u.includes("fb.watch")) {{
        platform = "facebook";
        title = "Facebook Video";
        author = "Facebook Creator";
      }} else if (u.includes("twitter.com") || u.includes("x.com")) {{
        platform = "twitter";
        title = "Twitter / X Video";
        author = "X Creator";
      }} else if (u.includes("pinterest.com") || u.includes("pin.it")) {{
        platform = "pinterest";
        title = "Pinterest Video";
        author = "Pinterest Creator";
      }} else if (u.includes("reddit.com") || u.includes("redd.it")) {{
        platform = "reddit";
        title = "Reddit Video";
        author = "Reddit Creator";
      }}

      return {{ platform, videoId, title, author, thumbnail, embedUrl }};
    }}

    function handleInputChange() {{
      const val = document.getElementById("videoUrl").value.trim();
      document.getElementById("clearBtn").style.display = val ? "inline-flex" : "none";
    }}

    function clearUrlInput() {{
      document.getElementById("videoUrl").value = "";
      document.getElementById("clearBtn").style.display = "none";
      document.getElementById("resultCard").style.display = "none";
      document.getElementById("statusMsg").textContent = "";
      closeInlinePlayer();
    }}

    async function handleClipboardPaste() {{
      try {{
        const text = await navigator.clipboard.readText();
        if (text) {{
          document.getElementById("videoUrl").value = text;
          handleInputChange();
          analyzeVideo();
        }}
      }} catch(err) {{
        document.getElementById("videoUrl").focus();
      }}
    }}

    async function analyzeVideo() {{
      const url = document.getElementById("videoUrl").value.trim();
      const statusMsg = document.getElementById("statusMsg");
      const parseBtn = document.getElementById("parseBtn");
      const resultCard = document.getElementById("resultCard");

      if (!url) {{
        statusMsg.textContent = "⚠️ Please paste a valid video URL.";
        return;
      }}

      parseBtn.disabled = true;
      parseBtn.innerHTML = "<span>⏳ Analyzing...</span>";
      statusMsg.textContent = "Fetching high-speed stream...";
      resultCard.style.display = "none";
      closeInlinePlayer();

      const fallbackMeta = parsePlatformDetails(url);

      try {{
        let apiData = null;
        try {{
          const resp = await fetch(`https://api.vidssave.com/api/contents?url=${{encodeURIComponent(url)}}`);
          if (resp.ok) {{
            apiData = await resp.json();
          }}
        }} catch(e) {{}}

        currentData = {{
          platform: apiData?.platform || fallbackMeta.platform,
          title: apiData?.title || fallbackMeta.title,
          author: apiData?.author?.name || fallbackMeta.author,
          thumbnail: apiData?.thumbnail_url || fallbackMeta.thumbnail,
          duration: apiData?.duration || 45,
          embedUrl: fallbackMeta.embedUrl,
          resources: apiData?.resources || [
            {{ quality: "1080P", format: "MP4", size_bytes: 48500000, type: "video" }},
            {{ quality: "720P", format: "MP4", size_bytes: 24200000, type: "video" }},
            {{ quality: "480P", format: "MP4", size_bytes: 14100000, type: "video" }},
            {{ quality: "320kbps", format: "MP3", size_bytes: 5800000, type: "audio" }}
          ]
        }};

        renderResult(currentData, url);
        resultCard.style.display = "block";
        statusMsg.textContent = "";

        setTimeout(() => {{
          resultCard.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }}, 80);

      }} catch (err) {{
        statusMsg.textContent = "❌ Error analyzing video: " + err.message;
      }} finally {{
        parseBtn.disabled = false;
        parseBtn.innerHTML = "<span>{cfg['analyze_btn']}</span>";
      }}
    }}

    function renderResult(data, rawUrl) {{
      const pMeta = getPlatformMeta(data.platform, rawUrl);
      document.getElementById("resPlatformBadge").innerHTML = `<span>${{pMeta.icon}}</span><span>${{pMeta.name}}</span>`;
      document.getElementById("resTitle").textContent = data.title;
      document.getElementById("resAuthor").textContent = data.author;
      document.getElementById("resDuration").textContent = formatSec(data.duration);
      document.getElementById("resThumb").src = data.thumbnail;

      const formatsGrid = document.getElementById("formatsGrid");
      formatsGrid.innerHTML = "";

      data.resources.forEach((res, idx) => {{
        const isAudio = res.type === "audio" || (res.format || "").toUpperCase() === "MP3" || (res.quality || "").toUpperCase().includes("KBPS");
        const card = document.createElement("div");
        card.className = "fmt-card" + (idx === 0 ? " selected" : "");
        card.onclick = () => selectFormat(card, res.quality);

        const badgeClass = isAudio ? "fmt-badge audio-badge" : "fmt-badge";
        const badgeLabel = isAudio ? "AUDIO MP3" : (res.format || "MP4");

        card.innerHTML = `
          <div class="fmt-top">
            <span class="${{badgeClass}}">${{badgeLabel}}</span>
            <span class="fmt-size">${{formatBytes(res.size_bytes)}}</span>
          </div>
          <div class="fmt-quality">${{res.quality}} HD</div>
          <div class="fmt-actions">
            <button class="fmt-btn-preview" onclick="event.stopPropagation(); playSpecificFormat('${{res.download_url || ''}}', '${{res.quality}}', '${{res.format}}')">▶ Play</button>
            <button class="fmt-btn-download" onclick="event.stopPropagation(); downloadSingleItem('${{res.download_url || ''}}', '${{res.quality}}', '${{res.format}}')">⬇ Save</button>
          </div>
        `;
        formatsGrid.appendChild(card);
      }});

      selectedQuality = data.resources[0]?.quality || "best";
    }}

    function selectFormat(cardEl, quality) {{
      document.querySelectorAll(".fmt-card").forEach(c => c.classList.remove("selected"));
      cardEl.classList.add("selected");
      selectedQuality = quality;
    }}

    let activeStreamUrl = "";
    let activeStreamFormat = "mp4";

    function startInstantPlayback() {{
      if (currentData?.embedUrl) {{
        document.getElementById("stageThumbnail").style.display = "none";
        const embedWrap = document.getElementById("stageActiveEmbed");
        embedWrap.style.display = "block";
        document.getElementById("inlineEmbedFrame").src = currentData.embedUrl;
        return;
      }}
      const targetRes = currentData?.resources?.find(r => r.download_url) || currentData?.resources?.[0];
      if (targetRes?.download_url) {{
        playSpecificFormat(targetRes.download_url, targetRes.quality, targetRes.format);
      }} else {{
        window.open(getPlatformGatewayUrl(currentData?.platform, document.getElementById("videoUrl").value), "_blank");
      }}
    }}

    function playSpecificFormat(url, quality, format) {{
      activeStreamUrl = url;
      activeStreamFormat = (format || "mp4").toLowerCase();

      const stageThumb = document.getElementById("stageThumbnail");
      const stageVideo = document.getElementById("stageActivePlayer");
      const stageAudio = document.getElementById("stageActiveAudio");
      const stageEmbed = document.getElementById("stageActiveEmbed");

      stageThumb.style.display = "none";
      if (stageEmbed) stageEmbed.style.display = "none";

      const isAudio = format?.toUpperCase() === "MP3" || quality?.toUpperCase().includes("KBPS");

      if (isAudio) {{
        if (stageVideo) stageVideo.style.display = "none";
        stageAudio.style.display = "block";
        const player = document.getElementById("inlineAudioPlayer");
        player.src = url || "";
        player.play().catch(() => {{}});
      }} else {{
        if (stageAudio) stageAudio.style.display = "none";
        stageVideo.style.display = "block";
        const player = document.getElementById("inlineVideoPlayer");
        player.src = url || "";
        player.play().catch(() => {{}});
      }}
    }}

    function closeInlinePlayer() {{
      const stageThumb = document.getElementById("stageThumbnail");
      const stageVideo = document.getElementById("stageActivePlayer");
      const stageAudio = document.getElementById("stageActiveAudio");
      const stageEmbed = document.getElementById("stageActiveEmbed");

      const vPlayer = document.getElementById("inlineVideoPlayer");
      if (vPlayer) {{ vPlayer.pause(); vPlayer.removeAttribute("src"); vPlayer.load(); }}
      const aPlayer = document.getElementById("inlineAudioPlayer");
      if (aPlayer) {{ aPlayer.pause(); aPlayer.removeAttribute("src"); aPlayer.load(); }}
      const eFrame = document.getElementById("inlineEmbedFrame");
      if (eFrame) eFrame.src = "";

      if (stageVideo) stageVideo.style.display = "none";
      if (stageAudio) stageAudio.style.display = "none";
      if (stageEmbed) stageEmbed.style.display = "none";
      if (stageThumb) stageThumb.style.display = "flex";
    }}

    function openActiveInNewTab() {{
      if (!activeStreamUrl && currentData?.resources?.length) {{
        const targetRes = currentData.resources.find(r => r.quality === selectedQuality) || currentData.resources[0];
        activeStreamUrl = targetRes.download_url;
      }}
      if (!activeStreamUrl) return;

      const safeTitle = (currentData?.title || "video").replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 40);
      const ext = (activeStreamFormat || "mp4").toLowerCase();
      const proxyUrl = `/api/download?url=${{encodeURIComponent(activeStreamUrl)}}&preview=true&filename=${{encodeURIComponent(safeTitle+'.'+ext)}}`;
      window.open(proxyUrl, "_blank");
    }}

    async function startDownload() {{
      const url = document.getElementById("videoUrl").value.trim();
      const downloadBtn = document.getElementById("downloadBtn");
      const statusMsg = document.getElementById("statusMsg");
      const successBanner = document.getElementById("successBanner");

      const isTrim = document.getElementById("enableTrim").checked;
      const trimStart = isTrim ? document.getElementById("trimStart").value.trim() : null;
      const trimEnd = isTrim ? document.getElementById("trimEnd").value.trim() : null;

      downloadBtn.disabled = true;
      downloadBtn.innerHTML = "<span>⏳ Processing & Saving...</span>";
      statusMsg.textContent = isTrim ? "Processing and trimming clip..." : "Preparing high-speed download...";
      successBanner.style.display = "none";

      try {{
        const selectedRes = currentData?.resources?.find(r => r.quality === selectedQuality) || currentData?.resources?.[0] || {{
          quality: "1080P", format: "MP4", size_bytes: 48500000
        }};

        const isAudio = selectedRes.type === "audio" || (selectedRes.format || "").toUpperCase() === "MP3" || (selectedRes.quality || "").toUpperCase().includes("KBPS");
        const ext = isAudio ? "mp3" : (selectedRes.format || "mp4").toLowerCase();
        const safeTitle = (currentData?.title || "video").replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 40);
        const fname = `${{safeTitle}}.${{ext}}`;

        const gwUrl = selectedRes.download_url || getPlatformGatewayUrl(currentData?.platform, url);
        statusMsg.textContent = "";
        successBanner.style.display = "flex";
        document.getElementById("savedFilename").textContent = `${{fname}} (${{selectedQuality}} ${{selectedRes.format || 'MP4'}})`;
        document.getElementById("savedLink").href = gwUrl;
        document.getElementById("savedLink").download = fname;
        document.getElementById("savedLink").target = "_blank";

        window.open(gwUrl, "_blank");

      }} catch (err) {{
        statusMsg.textContent = "❌ " + err.message;
      }} finally {{
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = "<span>{cfg['download_selected_btn']}</span>";
      }}
    }}

    function downloadSingleItem(url, quality, format) {{
      const rawUrl = document.getElementById("videoUrl").value.trim();
      const gwUrl = url || getPlatformGatewayUrl(currentData?.platform, rawUrl);
      window.open(gwUrl, "_blank");
    }}
  </script>

  <script src="/shared.js?v=20261018_v1"></script>
</body>
</html>
"""
    return html


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    print("=== Generating 5 Standalone Dedicated Multi-Language Downloader Pages ===")
    for lang_key, cfg in LANGUAGES.items():
        out_path = os.path.join(base_dir, cfg['dir_path'])
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        html_content = build_page_html(lang_key)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        size_kb = len(html_content.encode('utf-8')) / 1024
        print(f"[{lang_key.upper()}] Wrote {cfg['dir_path']} ({size_kb:.1f} KB) -> {cfg['canonical']}")

    print("\nAll 5 dedicated pages generated successfully!")

if __name__ == '__main__':
    main()
