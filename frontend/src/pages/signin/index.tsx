import { Response, request } from '@@/common/fetch';
import { AppBarComponent } from '@@/components/AppBar';
import { Label } from '@mui/icons-material';
import { AppBar, Box, Button, FormControl, Input, InputLabel, Toolbar, Typography } from '@mui/material';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

interface SignUp {
    name: string;
    password: string;
}

const SignInPage = () => {
  const router = useRouter();
  const [signup, setSignUp] = useState<SignUp>({name: '', password: ''});
  const [successMessage, setSuccessMessage] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleSubmit = async (event: any) => {
    event.preventDefault();
    try {
      const { data, error_message } = await request({
        url: "auth/signin",
        method: "POST",
        body: signup,
      }) as Response;
      if (data) {
        window.localStorage.setItem('access_token', data['access_token'])
        router.push('/')
      }
      else {
        setSuccessMessage('');
        setErrorMessage(error_message)
      }
    } catch (e) {
      setErrorMessage(`${e}`);
      setSuccessMessage('')
    }
  };

  const update = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    type: string
  ) => {
    if (type == 'name') {
      setSignUp((prev) => ({
        name: event.target.value,
        password: prev.password,
      }));
    } else if (type == 'password') {
      setSignUp((prev) => ({
        name: prev.name,
        password: event.target.value,
      }));
    }
  };

  return (
    <Box>
      <AppBarComponent />
      <Toolbar />
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          mt: 10,
        }}
      >
        <Typography variant="h4">로그인</Typography>
        <Box
          sx={{
            border: 1,
            borderColor: "#516dcb",
            borderRadius: 0.5,
            width: 300,
            p: 5,
          }}
        >
          <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{ mt: 3, display: "flex", flexDirection: "column" }}
          >
            <FormControl>
              <InputLabel>아이디</InputLabel>
              <Input
                id="sign-id"
                onChange={(event) => update(event, "name")}
              ></Input>
            </FormControl>
            <FormControl sx={{ mt: 5 }}>
              <InputLabel>패스워드</InputLabel>
              <Input
                id="sign-pw"
                type="password"
                onChange={(event) => update(event, "password")}
              />
            </FormControl>
            <Button
              sx={{ mt: 5 }}
              type="submit"
              variant="contained"
              color="primary"
            >
              로그인
            </Button>
            <Typography color="primary">{successMessage}</Typography>
            <Typography color="error">{errorMessage}</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default SignInPage;