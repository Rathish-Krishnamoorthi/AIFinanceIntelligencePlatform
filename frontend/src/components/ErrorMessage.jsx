import React from 'react';
import { Alert } from '@mui/material';
export default function ErrorMessage({ message }) { return message ? <Alert severity="error">{message}</Alert> : null; }
