from bot.upsell import UpsellManager


def test_voice_offer_trigger():
    upsell = UpsellManager(free_message_limit=3)
    user_id = 1
    for _ in range(3):
        upsell.record_message(user_id)
    assert upsell.needs_voice_offer(user_id)


def test_video_offer_after_voice():
    upsell = UpsellManager(free_message_limit=1)
    user_id = 2
    upsell.record_message(user_id)
    assert upsell.needs_voice_offer(user_id)
    upsell.record_voice_sent(user_id)
    assert upsell.needs_video_offer(user_id)
