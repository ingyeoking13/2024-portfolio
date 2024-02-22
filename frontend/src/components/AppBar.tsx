'use client'
import GitHubIcon from '@mui/icons-material/GitHub';
import Link from 'next/link';

import {
  Typography,
  Paper,
  AppBar,
  Toolbar,
  IconButton,
  Box,
  Menu,
  MenuItem,
  Button,
} from '@mui/material';
import { useEffect, useState } from 'react';
import { Response, request } from '@@/common/fetch';
import { useRouter } from 'next/navigation';

export const AppBarComponent = () => {
  const router = useRouter();
  const [anchorElement, setAnchorElement] = useState<null | HTMLElement>(null);
  const [loginStatus, setLoginStatus] = useState<boolean>(false);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElement(event.currentTarget);
  };

  const handleLogout = async () => {
    const { data } = (await request({
      url: "/auth/signout",
      method: "post",
      body: ''
    })) as Response;
    if (data) {
      window.localStorage.removeItem('access_token');
      window.location.reload();
    } else {
      alert('logout error.')
    }
  }

  useEffect(() => {
    const accessToken = window.localStorage.getItem('access_token')
    if(accessToken) {
      setLoginStatus(true);
    }
  },[])

  const repoUrl = 'https://github.com/ingyeoking13';
  return (
    <AppBar component="nav">
      <Toolbar>
        <Link href={repoUrl} target="_blank">
          <IconButton>
            <GitHubIcon htmlColor="#fff" />
          </IconButton>
        </Link>
        <Box>
          <Button
            onClick={handleClick}
            variant="contained"
            value={1}
            disableElevation
          >
            <Typography>인증</Typography>
          </Button>
          <Menu
            anchorEl={anchorElement}
            open={Boolean(
              anchorElement && anchorElement.getAttribute("value") == "1"
            )}
            onClose={() => setAnchorElement(null)}
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          >
            <MenuItem>
              <Button href="/signup" color="primary" LinkComponent={Link}>
                회원가입
              </Button>
            </MenuItem>
            {!loginStatus && (
              <MenuItem>
                <Button href="/signin" color="primary" LinkComponent={Link}>
                  로그인
                </Button>
              </MenuItem>
            )}
            {loginStatus && (
              <MenuItem>
                <Button onClick={handleLogout} color="primary">
                  로그아웃
                </Button>
              </MenuItem>
            )}
          </Menu>
        </Box>
        <Box>
          <Button
            onClick={handleClick}
            variant="contained"
            value={2}
            disableElevation
          >
            <Typography>처리율 제한 장치</Typography>
          </Button>
          <Menu
            anchorEl={anchorElement}
            open={Boolean(
              anchorElement && anchorElement.getAttribute("value") === "2"
            )}
            onClose={() => setAnchorElement(null)}
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          >
            <MenuItem>
              <Button
                href="/rate_limiter/token_bucket"
                color="primary"
                LinkComponent={Link}
              >
                토큰 버킷 알고리즘
              </Button>
            </MenuItem>
            <MenuItem>
              <Button
                href="/rate_limiter/leaky_bucket"
                color="primary"
                LinkComponent={Link}
              >
                누출 버킷 알고리즘
              </Button>
            </MenuItem>
          </Menu>
        </Box>
        <Box>
        <Button
            onClick={handleClick}
            variant="contained"
            value={3}
            disableElevation
          >
            <Typography>고유 아이디 생성기</Typography>
          </Button>
          <Menu
            anchorEl={anchorElement}
            open={Boolean(
              anchorElement && anchorElement.getAttribute("value") === "3"
            )}
            onClose={() => setAnchorElement(null)}
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          >
            <MenuItem>
              <Button
                href="/gen_id"
                color="primary"
                LinkComponent={Link}
              >
                snowflake token
              </Button>
            </MenuItem>
            </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}