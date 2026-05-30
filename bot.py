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

# SSL ওয়ার্নিং বন্ধ করা
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ⚙️ কনফিগারেশন প্যানেল ⚙️
# =========================================================================

ACCOUNT_FILE = "accounts.txt"             # আপনার অ্যাকাউন্টের টেক্সট ফাইল
PROXY_FILE = "proxies.txt"                # প্রক্সি ফাইল (গিটহাবে আইপি ব্লক এড়াতে)
MAX_CONCURRENT_BOTS = 20                  # একসাথে ২০টি অ্যাকাউন্ট চলবে
REWARD_LIMIT_PER_ACCOUNT = 1000           # প্রতি অ্যাকাউন্টে ১০০০ লিমিট

# আপনার দেওয়া অরিজিনাল অ্যাড লিংক এবং কুকিজ
DEFAULT_AD_URL = "https://googleads.g.doubleclick.net/mads/gma?submodel=sdk_gphone64_x86_64&adid_p=1&format=interstitial_mb&ini_pn=com.android.vending&ins_pn=com.android.vending&omid_v=a.1.5.2-google_20241009&client_purpose_one=true&dv=260480602&ev=23.6.0&gl=US&hl=en&js=afma-sdk-a-v260480999.244410000.1&lv=244410203&ms=CpgECoACKrBM0xB65xLcfKKUUNBRdQrRSSnKM5q33W3Rno1x7YXgQuyO29TZiieb9JHljSFyu3KaBD1cWyc5znE8zlF6grRJH4yzHz1M98-phMmdIeEPh7D2sR8hnkzi2v9526ZCvu0f5hnAuMwQcMH1EPA4tau9YROnTy3tMxLeQ2_YHxMMKWnbHD7DaItGYZpWUlNsJfnMhF9yVtIjcwiwRQshGpcTmM0ej1VO19P7ftW_kNnuMo99cuw_tejLzuKWBYFdepUFMdn8ve8sEshCSK_3ImHeln9JfRnFJ1vuVoPi1BxweXtJiCa9qY9o4sf-uWIm0aXlC2FcB0ibUr7qa2t-FAqAAh7NaFqVfQdJyoFCJWZUV7EGKmR8M-gSWzTHFNyUk4uif0z7EkZpHl4y78aHe_xfB8xwsqvl80VURdp1nRMa0MftZdgyPowdUbI9CyABv1VYHH_aP1AXwLJBKwjZxRux4Iz77UCMm1x0NmwhLPnlXJeFKC-329jAY4lHjcZ4DFczMFtt8j_vhO93rOusW_Ol7Q2uZGd_Um0CT1uV46o8bVSqZc35w_49SqGqiUKCayLq7uSGxv8-AqB-IsrVecNu9JIpCURFXVMRLcw8fbJP6xZ1ttzsjvgfvXBOKt1wpHJu-TArTBoTAxNBgY0ruKSpNVCzDkT_aYb9nCn3Y9-odIoSEO96QPNdRUBSHYFCwCc2GnQSmAQKgAKG9kguj6rc6JnqClGA11qHVt_GjKrOg_sjpO-CyHbF9iD-SflvbjkSb5mr65ZI-O1cCE4rj1EGGNQI9gobZLFvb07g_L88JpPZ_0HRCpNoVlgxr_TFYh5tufV7TCbHNFaVl9UWzBqvgbNr-4Vu_cAz0yJF3r2LA61fcDIXdhBIUqBcQfetYAzeoez4X_LYcgzYHV6DCODckYfj5BCj70-XyFXJh4Z-HhzQj6U5gD-1Cqt_Wz2Rr8GyUdzXRd_qtE7vek6OaMtTpjGzPy34dU6c1dlh_Gy9uT-iTylH_CU9KZoH39IFDnlCMsBwYI3jlPTAxfx56ToTIil_pFJnF73kCoACijWeZL6EluqVgSuoE5qUsRmlMTigQgSmQEsm6A96GxWTSu5OAthr8EfdF5pX1VZ1z7cYv7g6OWKT_M-F9H1atRx8e-qqwCoHWvQkMvW_7Lg8Sw7qaqDBDzbJ_L-YAhOKXaMw9gi0iSb_lc1mXqDXjOlYUutk0CVMCBJw951F-qEnGXRhAQyqG0y0BB6p7_lM9Bx5H8DRcjUzpUx69GjseaXdtSFn7zZTN1ufGjfdh4naxAyrcPwo6D3PpVSOFlMJkCmFXGnJzL8RgRpXwfuI91PzaW0YzKi2Y8rRzz0Us4iP99wHnmpsH2PecUDuISmahD-NfQCxUK5PFCgzmZ6CnRIQOO-0XSf0RqHDthMq1aBNLg&mv=85101930.com.android.vending&lft=1&vnm=1.2.5&plbs=0&plcs=0&risd=1&u_sd=2&request_id=1475162851&sam_b=24&sam_l=0&sam_r=0&sam_t=24&target_api=35&carrier=310260&request_agent=Flutter-GMA-5.3.1&fbs_aeid=-1763672715495716590&fbs_aiid=ed84d026b2efb0c47b9e7545b45685cf&seq_num=65&eid=318500618%2C318486317%2C318491267%2C95389098%2C318509511%2C318514156%2C95388544%2C318483611%2C318484496%2C318484801%2C318526144&guci=0.0.0.0.0.0.0.0&adtest=on&sdk_apis=7%2C8&omid_p=Google%2Fafma-sdk-a-v260480999.244410000.1&u_w=360&u_h=640&msid=com.m2e.mobile&an=123.android.com.m2e.mobile&u_audio=4&net=wi&u_so=p&rbv=1&loeid=44766145%2C318502924&preqs_in_session=2&preqs=64&time_in_session=868530&pcc=0&dload=18229&sst=1777580280000&output=html&region=mobile_app&u_tz=360&client=ca-app-pub-9027478617840640&slotname=9952810315&gsb=wi&apm_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&gmp_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&apm_app_type=1&lite=0&app_wp_code=ca-app-pub-9027478617840640&app_code=9535506442&num_ads=1&vpt=8&vfmt=18&vst=0&sdkv=o.260480999.244410000.1&sdmax=0&dmax=1&sdki=3c4d&stbg=1&bisch=false&blev=0.41&canm=true&_mv=85101930.com.android.vending&heap_free=445936&heap_max=201326592&heap_total=122484208&wv_count=4&advertised_mem_tier=0&avail_mem_tier=0&avail_proc_tier=0&rdps=11650&_cv=261434038&session_idl=20&eo_idl=36&eo_id_tsl=10&is_lat=false&rdidl=36&idtypel=4&blob=ABPQqLEabfpQcA59MgaPX1wtuBt_y7faAofi3bbFnsTYMjvMHAol2Pfu2xBE1dyari8Tpukq3mJ6d3C43sBjZa9dgkovrTzr_REfOnLqNH3LNQqxMcy0HLPBUgNXIleKhnv2eaJhmmL4DQtRAjKR-LSq1ug7tFIY2Jds7YRFkzFQNsJw_gCr_lEBIqPPzZlugiqMctfkSbWSXvkrxRan0zjBb1s0aRHee0rkPybj_jg9vB6BkZhiGUU7DT0hkf8iCVDQvT8TLi0fDYWnxDMOhsdV2K9eGbkv7QhZkIdta3q0kpaCDeWJy_LB3KzUu__ZZbtEiCEOEmhSjMm3nJzntJoogPuVKkYOT116k0GGgrW1ZjVBOYOX1CNkjdj27UIc4tAyEufZUtpeQI4bYb6EIcnpFw_GBoZ759M6mUNj_z8ROzDFs9VCZiWq1nLxGg&capsbf=7FFFFFEE&mr_itag=4509016882487189237_140&jsv=sdk_20190107_RC02-production-sdk_20260423_RC00"
DEFAULT_COOKIE = "IDE=AHWqTUmv5tx0LM4018aYpaP87TuE4_YOMKmgDrU0rj4CuPJY3-vPkfmvJjZIP7j2yWE"
DEFAULT_DRT = "CqwCCqcCRFNJRD1BSUNvaVlQRmgyY3gyaUpxMFNuZnMyVXM2SzMycWd2WTJmUDh6Q2hQdEdqV2NaVTZYQ216WjBUczZnUm9XTGJ6RzFIM2J3SEtNcUc2V3VXWnRCcEtaUTY5NXYzb3NRRVg5dVJ0bjhONkRBazJ4Tnhvckx3bU5PRUdJdXBHNnZQREFyYnZ3aDhIQmp3V1M5NWNRWTg4WnYxakIwLVVRZ1dqY1A2bmEtb1l0NUtMR216a2NGUHNzOW1Ca2lGRGNNWFhqMlJPek9BMy10M191ZEtoMVRwUnQ0UGpOaXk1OFBPQTFpZ2hIdnFzbTV5ZEMtdVRJYVlXaWVuY1dqWVdGUnFTdEZyOGJJTElqZURZcEFtdS1nOFlBYnNSX0FyZWlnNkZhURgB"

def log_msg(email, msg, symbol="ℹ️"):
    """গিটহাবের জন্য Flush=True যুক্ত ক্লিন লগিং ফাংশন"""
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{current_time}] [{email}] {symbol} {msg}", flush=True)

def load_accounts():
    accounts = []
    if not os.path.exists(ACCOUNT_FILE):
        print(f"❌ '{ACCOUNT_FILE}' ফাইলটি পাওয়া যায়নি!", flush=True)
        return accounts
        
    with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and parts[0].isdigit():
                accounts.append({"uid": parts[0], "email": parts[1]})
                
    return accounts

def load_proxies():
    proxies = []
    if not os.path.exists(PROXY_FILE):
        return proxies
    with open(PROXY_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            parts = line.split(":")
            if len(parts) == 4:
                host, port, user, pw = parts
                proxy_url = f"http://{user}:{pw}@{host}:{port}"
                proxies.append({"http": proxy_url, "https": proxy_url})
            elif len(parts) == 2:
                proxy_url = f"http://{parts[0]}:{parts[1]}"
                proxies.append({"http": proxy_url, "https": proxy_url})
    return proxies

def get_atok_data(uid):
    """আপনার অরিজিনাল লজিক (MISSION_AD)"""
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    data = {"key": f"{uid}{now}", "type": "MISSION_AD", "missionType": "VIDEO"}
    return urllib.parse.quote(json.dumps(data))

def run_bot(account, proxy_list):
    uid = account['uid']
    email = account['email']
    success_count = 0
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 15)',
        'X-Requested-With': 'com.m2e.mobile',
        'Cookie': DEFAULT_COOKIE,
        'X-Afma-Drt-V2-Cookie': DEFAULT_DRT,
        'Accept-Encoding': 'gzip'
    }

    log_msg(email, "রিওয়ার্ড যুক্ত করার বট চালু হয়েছে", "🚀")

    while success_count < REWARD_LIMIT_PER_ACCOUNT:
        proxy = random.choice(proxy_list) if proxy_list else None
        
        try:
            response = session.get(DEFAULT_AD_URL, headers=headers, proxies=proxy, verify=False, timeout=20)
            if response.status_code == 200:
                data = response.json()
                ad = data['ad_networks'][0]
                imp_url = ad['ad']['impression_urls'][0]
                start_url = ad['video_start_urls'][0]
                reward_url = ad['video_reward_urls'][0]
                
                # ইম্প্রেশন এবং স্টার্ট পিং
                session.get(imp_url, headers=headers, proxies=proxy, verify=False, timeout=15)
                session.get(start_url, headers=headers, proxies=proxy, verify=False, timeout=15)
                
                # আপনার অরিজিনাল ৬-৮ সেকেন্ডের বিরতি
                time.sleep(random.randint(6, 8))
                
                ts = str(int(time.time() * 1000))
                cdata = get_atok_data(uid)
                claim_url = reward_url.replace("@gw_rwd_userid@", uid).replace("@gw_tmstmp@", ts).replace("@gw_rwd_custom_data@", cdata)
                
                # রিওয়ার্ড ক্লেইম
                claim_res = session.get(claim_url, headers=headers, proxies=proxy, verify=False, timeout=15)
                
                if claim_res.status_code == 200:
                    success_count += 1
                    # শুধুমাত্র ৫০ টি কমপ্লিট হলে লগ প্রিন্ট করবে
                    if success_count % 50 == 0:
                        log_msg(email, f"রিওয়ার্ড যুক্ত হয়েছে! [{success_count}/{REWARD_LIMIT_PER_ACCOUNT}]", "✅")
                else:
                    pass
            else:
                time.sleep(3)
        except Exception:
            time.sleep(3)
            
        time.sleep(random.randint(2, 4))
        
    log_msg(email, "এই অ্যাকাউন্টের লিমিট শেষ হয়েছে।", "🏁")

def worker_thread(q, proxy_list):
    """Queue থেকে অ্যাকাউন্ট নিয়ে কাজ করবে"""
    while not q.empty():
        try:
            account = q.get_nowait()
        except queue.Empty:
            break
        run_bot(account, proxy_list)
        q.task_done()

def main():
    print("="*60, flush=True)
    print("🚀 ATOK 24/7 GITHUB ACTIONS BOT 🚀", flush=True)
    print("="*60, flush=True)
    
    accounts = load_accounts()
    proxies = load_proxies()

    if not accounts:
        print("❌ কোনো অ্যাকাউন্ট পাওয়া যায়নি। স্ক্রিপ্ট বন্ধ হচ্ছে।", flush=True)
        return
        
    print(f"✅ মোট {len(accounts)} টি অ্যাকাউন্ট লোড করা হয়েছে।", flush=True)
    if proxies:
        print(f"✅ মোট {len(proxies)} টি প্রক্সি লোড করা হয়েছে।", flush=True)
    print(f"✅ একসাথে {MAX_CONCURRENT_BOTS} টি অ্যাকাউন্ট চলবে।", flush=True)
    print("="*60, flush=True)

    q = queue.Queue()
    for acc in accounts:
        q.put(acc)

    threads = []
    num_threads = min(MAX_CONCURRENT_BOTS, len(accounts))
    
    for i in range(num_threads):
        t = threading.Thread(target=worker_thread, args=(q, proxies))
        t.start()
        threads.append(t)
        time.sleep(0.5)
        
    for t in threads:
        t.join()
        
    print("="*60, flush=True)
    print("🎉 সব অ্যাকাউন্টের কাজ সফলভাবে সম্পন্ন হয়েছে!", flush=True)
    print("="*60, flush=True)

if __name__ == "__main__":
    main()
