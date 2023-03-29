from config.config import SYNC_TO_DRAFT


def test():
    if SYNC_TO_DRAFT:
        print("11111111")
    else:
        print("2222222222")


if __name__ == '__main__':
    test()