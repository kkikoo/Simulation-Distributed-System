from pathlib import Path

code_of_message_type = {1:"CANCELLATION", -1:"CANCELLATION", 2:"ALERT", -2:"ALERT"}

def add_message(time, device_id, message_type, message_name, from_device):
    return time,device_id, message_type, message_name, from_device

def my_sort(ls):
    y = sorted(ls, key = lambda ele: (ele[0], ele[1], ele[2], ele[3], ele[4]))
    return y

def print_sent(time, device_id, message_type, to_id, message_name):
    print ("@{} #{}: SENT {} TO #{}: {}".format(time, device_id, code_of_message_type[message_type], to_id, message_name))

def print_received(time, device_id, message_type, from_id, message_name):
    print ("@{} #{}: RECEIVED {} TO #{}: {}".format(time, device_id, code_of_message_type[message_type], from_id, message_name))



def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def process_file(filepath):
    device = []
    next_device = {}
    cost_of_time = {}
    all_message_name = set()
    message_list = []

    try:
        #print filepath
        with open(filepath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0 or line[0] == '#':
                    continue
                word = line.split(' ')
                #print word
                if word[0] == 'DEVICE':
                    device.append(int(word[1]))
                elif word[0] == "PROPAGATE":
                    next_device[int(word[1])] = int(word[2])
                    cost_of_time[(int(word[1]), int(word[2]))] = int(word[3])
                elif word[0] == 'ALERT':
                    all_message_name.add(word[2])
                    message_list.append(add_message(int(word[3]), int(word[1]), 2, word[2], -1))
                else:
                    all_message_name.add(word[2])
                    message_list.append(add_message(int(word[3]), int(word[1]), 1, word[2], -1))
            return device, next_device, cost_of_time, all_message_name, message_list

    finally:
        print("FILE NOT FOUND")
        pass

def simulation(device, _next_device, cost_time, all_message_name, message_list):

    _from_device = {int(j): int(i) for i, j in _next_device.items()}
    known = {i: {j: False for j in device} for i in all_message_name}

    while len(message_list) > 0:
        # run first
        message_list = my_sort(message_list)
        first = message_list[0]
        message_list = message_list[1:]

        time, device_id, message_type, message_name, from_device = first[
            0], first[1], first[2], first[3], first[4]
        to_device_id = _next_device[device_id]
        from_device_id = _from_device[device_id]
        need_time = cost_time[(device_id, to_device_id)]

        #PRINT FIRST
        if from_device != -1:  #NOT FROM DEVICE, PRINT FIRST
            print_received(time, device_id, message_type,
                           from_device_id, message_name)

        # WHETHER PASS
        if message_type == 2:  # ALERT
            if known[message_name][device_id] == False:
                #ALERT CANCEL
                #KNOW AND SEND
                print_sent(time, device_id, message_type,
                           to_device_id, message_name)
                _message = add_message(  #RECEIVING
                    time=time + need_time,
                    device_id=to_device_id,
                    message_type=message_type,
                    message_name=message_name,
                    from_device=device_id
                )
                message_list.append(_message)
        else:  #CANCELATION
            if known[message_name][device_id] == False:

                print_sent(time, device_id, message_type,
                           to_device_id, message_name)
                _message = add_message(  #THEN RECEIVING
                    time=time + need_time,
                    device_id=to_device_id,
                    message_type=message_type,
                    message_name=message_name,
                    from_device=device_id
                )
                message_list.append(_message)
                known[message_name][device_id] = True #NOW, I KNOW

def main():
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    device, next_device, cost_of_time, all_message_name, message_list = process_file(input_file_path)
    simulation(device, next_device, cost_of_time, all_message_name, message_list)


if __name__ == '__main__':
    main()
