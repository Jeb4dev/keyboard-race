import { useContext } from 'react';
import { SocketContext } from './context';

export function useSocket() {
  return useContext(SocketContext);
}
