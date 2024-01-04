import { request } from '@@/common/fetch';
import { Label } from '@mui/icons-material';
import { Box, Button, FormControl, Input, InputLabel } from '@mui/material';
import React from 'react';

const SignInPage = () => {
  const handleSubmit = (event: any) => {
    event.preventDefault();
    request({
      url: 'signin',
      method: 'POST'
    } as Request)

  };
  return (
    <Box component="form" onSubmit={handleSubmit}>
      <FormControl>
        <InputLabel>아이디</InputLabel>
        <Input id="sign-id"></Input>
      </FormControl>
      <FormControl>
        <InputLabel>패스워드</InputLabel>
        <Input id="sign-pw" type="password"></Input>
      </FormControl>
      <Button type="submit" variant="contained" color="primary">
        로그인
      </Button>
    </Box>
  );
};

export default SignInPage;