import styles from './page.module.css';
import GitHubIcon from '@mui/icons-material/GitHub';
import Link from 'next/link';

import React from 'react';

import {Typography, Paper, AppBar, Toolbar, IconButton, Box} from '@mui/material';
import { AppBarComponent } from '@@/components/AppBar';

const Home = () => {
  return (
    <Paper className={styles.main}>
      <AppBarComponent />
      <Box>
        <Typography>
          Pod Status
        </Typography>
        <Typography>
          Pod Ip : ..
          namespace: ..

        </Typography>
      </Box>
    </Paper>
  );
}

export default Home;
