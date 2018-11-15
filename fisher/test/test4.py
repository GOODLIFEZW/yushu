key_map = {
            1: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            2: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            3: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            4: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            }
        }
print(key_map[1]['requester'])     # key_map[status][key]