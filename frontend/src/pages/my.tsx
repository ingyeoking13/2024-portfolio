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

const My: NextPage<any> = ({data}) => {

  return (
    <Box>
      <Typography>{JSON.stringify(data)}</Typography>
    </Box>
  );
};

export default My;
