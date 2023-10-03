'use client'
import React from 'react';

import {Typography, Paper, AppBar, Toolbar, IconButton} from '@mui/material';
import {Box} from '@mui/system';
import { PlayCircleFilledOutlined } from '@mui/icons-material';

const MainViewer = () => {

    const getCurrentPodsState = () => {
        console.log('hi!');
    };

  return (
    <Box>
      <IconButton onClick={getCurrentPodsState} >
        <PlayCircleFilledOutlined color='primary' />
      </IconButton>
    </Box>
  );
};

export default MainViewer;
