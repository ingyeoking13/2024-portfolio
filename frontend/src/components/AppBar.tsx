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
import { useState } from 'react';

export const AppBarComponent = () => {
  const [anchorElement, setAnchorElement] = useState<null | HTMLElement>(null);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElement(event.currentTarget);
  };

  const repoUrl = 'https://github.com/ingyeoking13';
  return (
    <AppBar>
      <Toolbar>
        <Link href={repoUrl} target="_blank">
          <IconButton>
            <GitHubIcon htmlColor="#fff" />
          </IconButton>
        </Link>
        <Box>
          <Button onClick={handleClick} variant="contained" disableElevation>
            <Typography>인증</Typography>
          </Button>
          <Menu
            anchorEl={anchorElement}
            open={Boolean(anchorElement)}
            onClose={() => setAnchorElement(null)}
            anchorOrigin={{vertical: 'bottom', horizontal: 'center'}}
          >
            <MenuItem>회원가입</MenuItem>
            <MenuItem>로그인</MenuItem>
            <MenuItem>로그아웃</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}