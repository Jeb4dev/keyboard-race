import React, { useEffect, useMemo, useState } from 'react';
import { useStore } from 'effector-react';
import { Button, Flex, Heading, Input, Text } from '@chakra-ui/react';

import { IRoom } from '../sockets/context';
import { useSocket } from '../sockets/useSocket';
import { leaveRace, startRace } from '../sockets/actions';
import StopDialog, { formatTime } from './StopDialog';
import { $users, fetchUser } from '../store/users';

interface RoomProps {
  roomId: number;
  room: IRoom;
  isOwner: boolean;
}

function Room({ room, roomId, isOwner }: RoomProps) {
  const { socket } = useSocket();
  const users = useStore($users);
  const [time, setTime] = useState(0);
  const [wordIndex, setWordIndex] = useState(0);
  const [correctness, setCorrectness] = useState<any>({});
  const [value, setValue] = useState('');
  const [finished, setFinished] = useState<boolean>(false);
  const [counterErrors, setCounterErrors] = useState(0);

  const [finishTime, setFinishTime] = useState(0);
  const [showDialog, setShowDialog] = useState(false);

  const onStart = () => startRace(socket);
  const words = useMemo(
    () =>
      room.words.words
        .split(' ')
        .map((v) => v.trim())
        .filter((v) => v.length > 0),
    [room.words],
  );

  useEffect(() => {
    if (room.started) {
      const timer = setInterval(() => {
        // @ts-ignore
        setTime(new Date() - new Date(room.time_start));
      }, 500);
      return () => {
        clearInterval(timer);
      };
    }
  }, [room.time_start, room.started]);

  useEffect(() => {
    const errors: any = {};
    words[wordIndex]
      .toLowerCase()
      .split('')
      .forEach((c, i) => {
        if (value[i] && c !== value[i].toLowerCase()) {
          errors[i] = true;
          setCounterErrors((counter) => counter + 1);
        } else if (value[i]) {
          errors[i] = false;
        }
      });
    setCorrectness(errors);
  }, [value]);

  useEffect(() => {
    if (words[wordIndex].toLowerCase() === value.toLowerCase()) {
      if (wordIndex + 1 === words.length) {
        console.log('end', counterErrors);
        setFinished(true);
        setFinishTime(time);
        setValue('');
        setShowDialog(true);
      } else {
        setWordIndex(wordIndex + 1);
        setValue('');
      }
    }
  }, [value]);

  return (
    <>
      <Heading textAlign="center">{room.room_title}</Heading>
      {showDialog && <StopDialog time={finishTime} count={words.length} errors={counterErrors} />}
      {!room.started &&
        (isOwner ? (
          <Flex>
            <Button onClick={onStart}>Start</Button>
          </Flex>
        ) : (
          <Text>Wait for owner for start</Text>
        ))}
      {room.started && !finished && <Text>Time since start: {time === 0 ? '00:00' : formatTime(time)}</Text>}

      {!finished && (
        <>
          <Heading textAlign="center">
            {words[wordIndex].split('').map((v, i) => (
              <span
                style={{
                  color: correctness[i] === true ? 'red' : correctness[i] === false ? 'green' : '',
                }}
              >
                {v}
              </span>
            ))}
          </Heading>
          <Input
            variant="outline"
            placholder="Type word here"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            maxLength={words[wordIndex].length}
            isDisabled={!room.started}
          />
          <Text fontSize="2xl" textAlign="left" color="gray">
            {room.words.words}
          </Text>
          <Heading>Room members</Heading>
          {room.users.map((v) => {
            let name = '' + v;
            if (users[v]) {
              name = '' + users[v];
            } else {
              fetchUser(v);
            }
            return <Text>{name}</Text>;
          })}
        </>
      )}
    </>
  );
}

export default Room;
