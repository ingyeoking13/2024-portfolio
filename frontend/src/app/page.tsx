import styles from './page.module.css';
import { Typography, Paper, AppBar, Toolbar, IconButton, Box } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import Link from 'next/link';

import React, {useEffect, useState} from 'react';

import {Typography, Paper, AppBar, Toolbar, IconButton} from '@mui/material';
import {Box} from '@mui/system';
import {PlayCircleFilledOutlined} from '@mui/icons-material';
import {Request} from '@@/common/fetch';
import {NextPage, NextPageContext} from 'next';

const dashboardQuery = async () => {
  const res = await Request<any>('/dashboard');
  return res['message'];
};

export const getServerSideProps = async () => {
  try{
    const g = await dashboardQuery();
    return {
      props: {
        data: g
      },
    };
  } catch (e) {
    return {
      props: {
        data: null
      }
    }
  }
};
const Home = ({data}: {data : any}) => {
  const repoUrl = 'https://github.com/ingyeoking13'
  return (
    <Paper className={styles.main}>
      <AppBar>
        <Toolbar >
          <Link href={repoUrl} target='_blank'>
            <IconButton>
              <GitHubIcon htmlColor='#fff' />
            </IconButton>
          </Link>
          <Link href='/my'>hi</Link>
        </Toolbar>
      </AppBar>
      <Box>
        <Typography>
          Pod Status
        </Typography>
        <Typography>
          Phase : { JSON.stringify(data) }
          Pod Ip : ..
          namespace: ..

        </Typography>
      </Box>
    </Paper>
  );
}

export default Home;
