import styles from './page.module.css';
import { Typography, Paper, AppBar, Toolbar, IconButton } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import Link from 'next/link';

export default function Home() {
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
    </Paper>
  );
}
