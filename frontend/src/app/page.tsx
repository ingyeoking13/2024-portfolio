import Image from 'next/image';
import styles from './page.module.css';
import { Typography, Paper, AppBar, Toolbar, IconButton } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import MainViewer from '@@/MainViewer/MainViewer';

export default function Home() {
  return (
    <Paper className={styles.main}>
      <AppBar>
        <Toolbar >
          <IconButton>
            <GitHubIcon htmlColor='#fff' />
          </IconButton>
        </Toolbar>
      </AppBar>
      <MainViewer />
    </Paper>
  );
}
