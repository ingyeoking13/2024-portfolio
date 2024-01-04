import styles from './page.module.css';
import GitHubIcon from '@mui/icons-material/GitHub';
import Link from 'next/link';

import React, {useEffect, useState} from 'react';

import {Typography, Paper, AppBar, Toolbar, IconButton, Box} from '@mui/material';
import {PlayCircleFilledOutlined} from '@mui/icons-material';
import {request} from '@@/common/fetch';
import {NextPage, NextPageContext} from 'next';
import { AppBarComponent } from '@@/components/AppBar';

const dashboardQuery = async () => {
  const res = await request<any>('/dashboard');
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
  return (
    <Paper className={styles.main}>
      <AppBarComponent />
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
