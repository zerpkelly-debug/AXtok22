# -*- coding: utf-8 -*-
import requests
import threading
import time
import json
import urllib.parse
import datetime
import urllib3
import random
import queue
import os
import re
from concurrent.futures import ThreadPoolExecutor

# SSL ওয়ার্নিং বন্ধ করা
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================================
# ⚙️ কনফিগারেশন প্যানেল ⚙️
# =========================================================================

ACCOUNT_FILE = "accounts.txt"             # আপনার অ্যাকাউন্টের টেক্সট ফাইল
MAX_CONCURRENT_BOTS = 20                  # একসাথে কতগুলো অ্যাকাউন্ট চলবে
REWARD_LIMIT_PER_ACCOUNT = 1000           # প্রতি অ্যাকাউন্টে লিমিট
MIN_AD_DELAY = 2                          # একটি অ্যাড দেখার পর সর্বনিম্ন অপেক্ষা (সেকেন্ড)
MAX_AD_DELAY = 4                          # সর্বোচ্চ অপেক্ষা (সেকেন্ড)

# ডিফল্ট কুকিজ এবং হেডার ডেটা
DEFAULT_COOKIE = "IDE=AHWqTUmv5tx0LM4018aYpaP87TuE4_YOMKmgDrU0rj4CuPJY3-vPkfmvJjZIP7j2yWE"
DEFAULT_DRT = "AICoiYOkO_zvNeR0SAqE9ciDuzu4ROzD5M_h6bWR-jRQqz2ecWVHMuFytCRZ2EMBthrpGxJCHdhSO-gZimPDzWmoKU7V5bcsoXhKRUHHQH8lUGMmGnTp-xCP2Np9W73-LshmiC0y1vN33tqKW9elp9vnqP96g5mK3IcJTE8RVJjhTTaoWxvS_yTsnm9P3fnwLMu3R5FA_ucj0uu2pvQUXJX7y2jEH2h5pwTgUqVn2w7HhwTodRVqboXhL0ZAu85T6Sm6lMg7kVILH2emmPF_V6qiBSSg_92bqA"

GMA_URL_BASE = "https://googleads.g.doubleclick.net/mads/gma?submodel=sdk_gphone64_x86_64&adid_p=1&format=interstitial_mb&ini_pn=com.android.vending&ins_pn=com.android.vending&omid_v=a.1.5.2-google_20241009&client_purpose_one=true&dv=260480602&ev=23.6.0&gl=US&hl=en&js=afma-sdk-a-v260480999.244410000.1&lv=244410203&ms=CpgECoACKrBM0xB65xLcfKKUUNBRdQrRSSnKM5q33W3Rno1x7YXgQuyO29TZiieb9JHljSFyu3KaBD1cWyc5znE8zlF6grRJH4yzHz1M98-phMmdIeEPh7D2sR8hnkzi2v9526ZCvu0f5hnAuMwQcMH1EPA4tau9YROnTy3tMxLeQ2_YHxMMKWnbHD7DaItGYZpWUlNsJfnMhF9yVtIjcwiwRQshGpcTmM0ej1VO19P7ftW_kNnuMo99cuw_tejLzuKWBYFdepUFMdn8ve8sEshCSK_3ImHeln9JfRnFJ1vuVoPi1BxweXtJiCa9qY9o4sf-uWIm0aXlC2FcB0ibUr7qa2t-FAqAAh7NaFqVfQdJyoFCJWZUV7EGKmR8M-gSWzTHFNyUk4uif0z7EkZpHl4y78aHe_xfB8xwsqvl80VURdp1nRMa0MftZdgyPowdUbI9CyABv1VYHH_aP1AXwLJBKwjZxRux4Iz77UCMm1x0NmwhLPnlXJeFKC-329jAY4lHjcZ4DFczMFtt8j_vhO93rOusW_Ol7Q2uZGd_Um0CT1uV46o8bVSqZc35w_49SqGqiUKCayLq7uSGxv8-AqB-IsrVecNu9JIpCURFXVMRLcw8fbJP6xZ1ttzsjvgfvXBOKt1wpHJu-TArTBoTAxNBgY0ruKSpNVCzDkT_aYb9nCn3Y9-odIoSEO96QPNdRUBSHYFCwCc2GnQSmAQKgAKG9kguj6rc6JnqClGA11qHVt_GjKrOg_sjpO-CyHbF9iD-SflvbjkSb5mr65ZI-O1cCE4rj1EGGNQI9gobZLFvb07g_L88JpPZ_0HRCpNoVlgxr_TFYh5tufV7TCbHNFaVl9UWzBqvgbNr-4Vu_cAz0yJF3r2LA61fcDIXdhBIUqBcQfetYAzeoez4X_LYcgzYHV6DCODckYfj5BCj70-XyFXJh4Z-HhzQj6U5gD-1Cqt_Wz2Rr8GyUdzXRd_qtE7vek6OaMtTpjGzPy34dU6c1dlh_Gy9uT-iTylH_CU9KZoH39IFDnlCMsBwYI3jlPTAxfx56ToTIil_pFJnF73kCoACijWeZL6EluqVgSuoE5qUsRmlMTigQgSmQEsm6A96GxWTSu5OAthr8EfdF5pX1VZ1z7cYv7g6OWKT_M-F9H1atRx8e-qqwCoHWvQkMvW_7Lg8Sw7qaqDBDzbJ_L-YAhOKXaMw9gi0iSb_lc1mXqDXjOlYUutk0CVMCBJw951F-qEnGXRhAQyqG0y0BB6p7_lM9Bx5H8DRcjUzpUx69GjseaXdtSFn7zZTN1ufGjfdh4naxAyrcPwo6D3PpVSOFlMJkCmFXGnJzL8RgRpXwfuI91PzaW0YzKi2Y8rRzz0Us4iP99wHnmpsH2PecUDuISmahD-NfQCxUK5PFCgzmZ6CnRIQOO-0XSf0RqHDthMq1aBNLg&mv=85152130.com.android.vending&lft=1&vnm=1.2.5&plbs=0&plcs=0&risd=1&u_sd=2&request_id={REQ_ID}&sam_b=0&sam_l=0&sam_r=0&sam_t=0&target_api=35&carrier=310260&request_agent=Flutter-GMA-5.3.1&fbs_aeid={FBS_AEID}&fbs_aiid=ed84d026b2efb0c47b9e7545b45685cf&seq_num={SEQ_NUM}&eid=318500618%2C318486317%2C318491267%2C95391602%2C318503826%2C318527161%2C318528038%2C318528076%2C95388545%2C318483611%2C318484496%2C318484801%2C318526145%2C318526849%2C318527070&guci=0.0.0.0.0.0.0.0&adtest=on&sdk_apis=7%2C8&omid_p=Google%2Fafma-sdk-a-v260480999.244410000.1&u_w=360&u_h=640&msid=com.m2e.mobile&an=123.android.com.m2e.mobile&dvoln=1&u_audio=4&net=wi&u_so=p&rbv=1&loeid=44766145%2C318502621&preqs_in_session=30&preqs=30&time_in_session=2435490&pcc=0&dload=3593&sst=1780127340000&output=html&region=mobile_app&u_tz=360&client=ca-app-pub-9027478617840640&slotname=9273929755&gsb=wi&apm_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&gmp_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&apm_app_type=1&lite=0&app_wp_code=ca-app-pub-9027478617840640&app_code=9535506442&num_ads=1&vpt=8&vfmt=18&vst=0&sdkv=o.260480999.244410000.1&sdmax=0&dmax=1&sdki=3c4d&stbg=1&bisch=false&blev=0.41&canm=true&_mv=85152130.com.android.vending&heap_free=22952032&heap_max=201326592&heap_total=56697760&wv_count=1&a_ad_mem=8000000000&a_avai=2426978304&a_total=4110749696&a_threshold=226492416&a_is_low_mem=false&runtime_avai_processors=4&advertised_mem_tier=6&avail_mem_tier=4&avail_proc_tier=3&rdps=4500&session_idl=20&eo_idl=36&eo_id_tsl=10&is_lat=false&rdidl=36&idtypel=4&blob=ABPQqLGyGdWgnKVO9yp3KC0KqDzG99j5XaYslgMJ2bsVmW7TD23HbH3wBiKWM163-nNTC39faMyH-eeWPdblVHrIXBsLWwB52h0czsAwEUxrbcW6My5YTN5Xn8JmCX098MAGN6cpEkH4010tIkqHFKVjxnFnzd0rCM4eK_EHvms0Fi5LlwBcEiO52PXswgmdufcQ3Nmw-CLzWxW6GT_sVNiCyeqyQaomNHLF2erq7NFCekTPONLrKgNng6pHIHVcQm57wmW3e6Q3RzB78WLj3RUdb7DDAYT8P6ZAZyjmx0sQfi5HbHH93RDI5ZnbwjWhlFUNPSbbyArRSW-IU5yCH72c8X6FKEe0CX37lUvUzF3RSWFddaYQ4r3BEFvYAoRHuqPqMchVZXyeQmYt8DL0WPPWwnybxkwtvaFsrJoj_yvKDlpzJ7jog5edYbAB1w&capsbf=7FFFFFEE&jsv=sdk_20190107_RC02-production-sdk_20260520_RC00"

GOOGLE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; sdk_gphone64_x86_64 Build/AE3A.240806.036; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/148.0.7778.120 Mobile Safari/537.36 (Mobile; afma-sdk-a-v260480999.244410000.1)",
    "X-Requested-With": "com.m2e.mobile",
    "Cookie": f"IDE={DEFAULT_COOKIE}",
    "x-afma-drt-v2-cookie": DEFAULT_DRT,
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://googleads.g.doubleclick.net/",
    "Connection": "Keep-Alive"
}

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def log_msg(email, msg):
    """শুধুমাত্র নির্দিষ্ট মেসেজ প্রিন্ট করার জন্য ক্লিন লগার"""
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{current_time}] [{email}] {msg}")

def load_accounts():
    """accounts.txt থেকে UID এবং Email লোড করা"""
    accounts = []
    if not os.path.exists(ACCOUNT_FILE):
        print(f"❌ '{ACCOUNT_FILE}' ফাইলটি পাওয়া যায়নি! দয়া করে ফাইলটি তৈরি করুন।")
        return accounts
        
    with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and parts[0].isdigit():
                accounts.append({"uid": parts[0], "email": parts[1]})
                
    return accounts

def get_dynamic_gma_url():
    """গুগলের অ্যাড রিকুয়েস্ট প্যারামিটার র‍্যান্ডমাইজ করা"""
    req_id = str(random.randint(1000000000, 2000000000))
    seq_num = str(random.randint(20, 150))
    fbs_aeid = str(random.randint(1000000000000000000, 9000000000000000000))
    return GMA_URL_BASE.replace("{REQ_ID}", req_id).replace("{SEQ_NUM}", seq_num).replace("{FBS_AEID}", fbs_aeid)

def get_atok_data(uid):
    """Atok এর CHECKIN_AD JSON পেলোড"""
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    data = {"key": f"{uid}{now}", "type": "CHECKIN_AD", "checkInSequence": 1}
    return urllib.parse.quote(json.dumps(data, separators=(',', ':')))

def decode_html_content(html_str):
    """VAST HTML ডিকোড"""
    return html_str.replace(r'\x3c', '<').replace(r'\x3e', '>').replace(r'\x3d', '=').replace(r'\x22', '"').replace(r'\x26', '&').replace(r'\x27', "'")

def format_url(url, uid):
    """লিংকের ম্যাক্রো ভ্যালু রিপ্লেস"""
    current_time_ms = str(int(time.time() * 1000))
    atok_cdata = get_atok_data(uid)
    
    url = url.replace("@gw_rwd_userid@", str(uid))
    url = url.replace("@gw_tmstmp@", current_time_ms)
    url = url.replace("@gw_rwd_custom_data@", atok_cdata)
    url = url.replace("@gw_adnetstatus@", "0")
    url = url.replace("@gw_ttr@", "245")
    url = url.replace("@gw_mpe@", "0")
    
    url = url.replace("%5BVIEWABILITY%5D", "1").replace("%5BGOOGLE_VIEWABILITY%5D", "1")
    url = url.replace("[VIEWABILITY]", "1").replace("[GOOGLE_VIEWABILITY]", "1")
    url = url.replace("[ACTTYPE]", "1").replace("%5BAD_MT%5D", "12")
    url = url.replace("%5BAD_TOS%5D", "10000,0,0,0,0").replace("%5BAD_WAT%5D", "10")
    url = url.replace("%5BFINAL%5D", "1")
    return url

def get_xml_urls(event_name, html):
    pattern = r'<Tracking event="' + event_name + r'">\s*<!\[CDATA\[(.*?)\s*\]\]>\s*</Tracking>'
    return re.findall(pattern, html)

def get_video_duration(html):
    match = re.search(r'<Duration>(.*?)</Duration>', html)
    if match:
        time_str = match.group(1).strip()
        try:
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        except: pass
    return 30.0

def send_ad_pings(session, url_list, uid):
    """গুগলের সার্ভারে ট্র্যাকিং সিগন্যাল পাঠানো (নীরবে)"""
    if not url_list: return False
    success = False
    for url in url_list:
        if not url: continue
        clean_url = format_url(url, uid)
        try:
            res = session.get(clean_url, timeout=10)
            if res.status_code in [200, 204]:
                success = True
        except Exception: pass
    return success

# =========================================================================
# 🤖 কোর বট ওয়ার্কার (Google Anti-Fraud Bypass) 🤖
# =========================================================================
def run_bot(account):
    uid = account['uid']
    email = account['email']
    success_count = 0
    
    session = requests.Session()
    session.headers.update(GOOGLE_HEADERS)

    # কাজ শুরুর লগ
    log_msg(email, "রিওয়ার্ড যুক্ত করার বট চালু হয়েছে")

    while success_count < REWARD_LIMIT_PER_ACCOUNT:
        dynamic_url = get_dynamic_gma_url()
        try:
            # 1. Fetch Ad
            response = session.get(dynamic_url, verify=False, timeout=15)
            if response.status_code != 200:
                time.sleep(5)
                continue

            ad_data = response.json()
            network = ad_data.get('ad_networks', [{}])[0]
            ad_info = network.get('ad', {})
            ad_html = decode_html_content(ad_info.get('ad_html', ''))
            
            fill_urls = network.get('fill_urls', [])
            impression_urls = network.get('impression_urls', [])
            video_start_urls = network.get('video_start_urls', [])
            video_complete_urls = network.get('video_complete_urls', [])
            reward_urls = network.get('video_reward_urls', [])
            
            if not reward_urls:
                time.sleep(2)
                continue

            impression_xml = re.findall(r'<Impression><!\[CDATA\[(.*?)\]\]></Impression>', ad_html)
            start_xml = get_xml_urls("start", ad_html)
            q25 = get_xml_urls("firstQuartile", ad_html)
            q50 = get_xml_urls("midpoint", ad_html)
            q75 = get_xml_urls("thirdQuartile", ad_html)
            complete_xml = get_xml_urls("complete", ad_html)
            active_views = re.findall(r'<Tracking event="(?:viewable_impression|measurable_impression|fully_viewable_audible_half_duration_impression)"><!\[CDATA\[(.*?)\]\]></Tracking>', ad_html)
            
            ad_duration = get_video_duration(ad_html)
            split_time = ad_duration / 4.0

            # 2. Pings & Watch Time Simulation
            send_ad_pings(session, fill_urls, uid)
            send_ad_pings(session, impression_urls, uid)
            send_ad_pings(session, impression_xml, uid)

            time.sleep(1)
            send_ad_pings(session, video_start_urls, uid)
            send_ad_pings(session, start_xml, uid)
            send_ad_pings(session, active_views, uid)

            time.sleep(split_time)
            send_ad_pings(session, q25, uid)
            
            time.sleep(split_time)
            send_ad_pings(session, q50, uid)
            
            time.sleep(split_time)
            send_ad_pings(session, q75, uid)
            
            time.sleep(split_time)
            send_ad_pings(session, complete_xml, uid)
            send_ad_pings(session, video_complete_urls, uid)

            time.sleep(2)
            
            # 3. Request Reward
            if send_ad_pings(session, reward_urls, uid):
                success_count += 1
                
                # শুধুমাত্র প্রতি ৫০টা কমপ্লিট হলে মেসেজ প্রিন্ট করবে
                if success_count % 50 == 0:
                    log_msg(email, f"✅ রিওয়ার্ড যুক্ত হয়েছে! [{success_count}/{REWARD_LIMIT_PER_ACCOUNT}]")

        except Exception:
            time.sleep(5)
        
        # পরবর্তী অ্যাডের আগে রেন্ডম বিরতি
        delay = random.randint(MIN_AD_DELAY, MAX_AD_DELAY)
        time.sleep(delay)
        
    log_msg(email, "এই অ্যাকাউন্টের লিমিট শেষ হয়েছে, বট বন্ধ হচ্ছে।")

# =========================================================================
# কিউ (Queue) ভিত্তিক মাল্টি-থ্রেডিং ম্যানেজার
# =========================================================================
def worker_thread(q):
    """ওয়ার্কার থ্রেড যা কিউ থেকে অ্যাকাউন্ট নেবে এবং কাজ করবে"""
    while not q.empty():
        try:
            account = q.get_nowait()
        except queue.Empty:
            break
        
        # বট রান করানো
        run_bot(account)
        q.task_done()

def main():
    print("="*60)
    print("🚀 ATOK PRO MULTI-BOT V3 (HEADLESS / 24/7 MODE) 🚀")
    print("="*60)
    
    accounts = load_accounts()
    if not accounts:
        print("❌ স্ক্রিপ্ট বন্ধ হচ্ছে।")
        return
        
    print(f"✅ মোট {len(accounts)} টি অ্যাকাউন্ট লোড করা হয়েছে।")
    print(f"✅ একসাথে {MAX_CONCURRENT_BOTS} টি অ্যাকাউন্ট চলবে।")
    print("="*60)

    # সব অ্যাকাউন্ট কিউ-তে রাখা হচ্ছে
    q = queue.Queue()
    for acc in accounts:
        q.put(acc)

    # লিমিট অনুযায়ী থ্রেড তৈরি করা
    threads = []
    num_threads = min(MAX_CONCURRENT_BOTS, len(accounts))
    
    for i in range(num_threads):
        t = threading.Thread(target=worker_thread, args=(q,))
        t.start()
        threads.append(t)
        time.sleep(0.5) # থ্রেডগুলোর শুরুর মধ্যে হালকা গ্যাপ
        
    # সব কাজ শেষ হওয়ার জন্য অপেক্ষা করা
    for t in threads:
        t.join()
        
    print("="*60)
    print("🎉 সব অ্যাকাউন্টের কাজ সফলভাবে সম্পন্ন হয়েছে!")
    print("="*60)

if __name__ == "__main__":
    main()
