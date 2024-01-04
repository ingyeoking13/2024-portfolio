import { request } from '@@/common/fetch';
import { Label } from '@mui/icons-material';
import { Box, Button, FormControl, Input, InputLabel } from '@mui/material';
import React, { useState } from 'react';

interface SignUp {
    id: string;
    password: string;
}

const SignInPage = () => {
  const [signup, setSignUp] = useState<SignUp>({id: '', password: ''});

  const handleSubmit = async (event: any) => {
    event.preventDefault();
    const result = await request({
      url: 'signup',
      method: 'POST',
      body: signup,
    })
  };

  const update = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    type: string
  ) => {
    if (type == 'id') {
      setSignUp((prev) => ({
        id: event.target.value,
        password: prev.password,
      }));
    } else if (type == 'password') {
      setSignUp((prev) => ({
        id: prev.id,
        password: prev.password,
      }));
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <FormControl>
        <InputLabel>아이디</InputLabel>
        <Input id="sign-id" onChange={(event) => update(event, 'id')}></Input>
      </FormControl>
      <FormControl>
        <InputLabel>패스워드</InputLabel>
        <Input id="sign-pw" type="password"></Input>
      </FormControl>
      <Button type="submit" variant="contained" color="primary">
        회원가입
      </Button>
    </Box>
  );
};

export default SignInPage;