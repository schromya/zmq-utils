from zmq_utils.logger import Logger

import time
import json
from pathlib import Path

import zmq


HOST = '127.0.0.1'

def test_pub_sub_logging(tmp_path:Path):
    """
    Test for pub/sub logging
    """
    # Setup a PUB socket to send test messages
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUB)
    port = pub.bind_to_random_port(f'tcp://{HOST}')
    time.sleep(0.5) 
    
    log_path = tmp_path / 'log.json'
    logger = Logger(HOST, port, 'pub_sub', str(log_path))
    logger.run_threaded_logger()
    time.sleep(0.5)
    
    
    pub.send_multipart([b'test topic', b'test message 1'])
    pub.send_multipart([b'test topic', b'test message 2'])
    time.sleep(1)
    
    # Check that the log file was written and contains correct fields
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = [json.loads(line) for line in lines]

    assert len(entries) >= 1, "No data was logged."
    assert len(entries) >= 2, "Only the manifest (not any data) was logged. "

    m = entries[0]
    r1 = entries[1]
    r2 = entries[2]
    assert m.get('socket_pattern') == 'pub_sub', f"pub_sub not found in socket_pattern of manifest."
    
    correct_record = False
    if (r1.get('topic') == 'test topic' and
        'test message 1' in ''.join(r1.get('frames', [])) and
        r1.get('socket_pattern') == 'pub_sub'):
        correct_record = True
    assert correct_record, "Expected topic, message, and socket_pattern not found in record 1."
    
    correct_record = False
    if (r2.get('topic') == 'test topic' and
        'test message 2' in ''.join(r2.get('frames', [])) and
        r2.get('socket_pattern') == 'pub_sub'):
        correct_record = True
    assert correct_record, "Expected topic, message, and socket_pattern not found in record 2."
    
    # Cleanup
    logger.shutdown()
    pub.close()
    ctx.term()
