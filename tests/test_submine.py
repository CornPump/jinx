import pytest
import submine
import os


# Make sure credentials are valid every build!
def test_validate_reddit_credentials():
    ins = submine.Submine("BitcoinMarkets", "daily", 100,os.getcwd())
    assert ins.validate_reddit_credentials() == True


@pytest.mark.parametrize("sub_name, post_name, limit, origin_dir", [
    ("BitcoinMarkets", "daily", 100,os.getcwd()),
    ("BitcoinMarkets", "daily", submine.REDDIT_THREAD_LIMIT + 100,os.path.join(os.getcwd(),'random_dir_name')),
    ("BitcoinMarkets", "daily", 0,''),
    ("BitcoinMarkets", "daily", -50,''),
])
def test_submine_instance_params(sub_name, post_name, limit, origin_dir):
    ins = submine.Submine(sub_name=sub_name, post_name=post_name, limit=limit,origin_dir=origin_dir)
    assert ins.sub_name == sub_name
    assert ins.post_name == post_name
    if limit == None:
        assert ins.limit == None
    else:
        if limit >= submine.REDDIT_THREAD_LIMIT:
            assert ins.limit == None
        elif limit > 0 and limit < submine.REDDIT_THREAD_LIMIT:
            assert limit == ins.limit
        else:
            assert ins.limit == 1
    if not origin_dir:
        assert ins.origin_dir == os.getcwd()
    elif os.path.exists(origin_dir):
        assert ins.origin_dir == origin_dir
    else:
        assert ins.origin_dir == os.getcwd()


