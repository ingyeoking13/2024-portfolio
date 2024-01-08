
import { RayEventResponse, Response, request } from '@@/common/fetch';
import { AppBarComponent } from '@@/components/AppBar';
import { Label } from '@mui/icons-material';
import { AppBar, Box, Button, FormControl, Input, InputLabel, TextField, Toolbar, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import _ from 'lodash';
import { unixToUtc } from '@@/common/utils';

const TokenBucketPage = () => {
    const [tokenId, setTokenId] = useState<string>('');
    const [log, setLog] = useState<string>('');

    const handleSubmit = async (
      event: any
    ) => {
      event.preventDefault();
      const { data } = (await request({
        url: "/rate_limiter/token_bucket",
        method: "POST",
        body: "",
      })) as Response;
      if (data) {
        setTokenId(data);
      }
    };

    useEffect(()=>{
        setLog('')
        if (!tokenId) return;
        const ws = new WebSocket(
          `ws://localhost/api/v1/rate_limiter/status/token_bucket?id=${tokenId}`
        );

        // Listen for messages
        ws.addEventListener('message', function (event) {
            // console.log(log);
            const result = JSON.parse(event.data) as RayEventResponse[];
            const logs = _.map(
              result,
              (item) =>
                `[${unixToUtc(parseInt(item.time))}] [${item.name}] [${item.status}] [${item.result}]`
            );

            // const g =
            //   /\[(?<time>\w+)\]\s\[(?<name>[\w\-]+)\]\s\[(?<status>\w+)\]\s\[(?<result>\w+)\]/;

            if (result[result.length-1].result == 'fin') {
              ws.close();
            } 
            const appending = _.reduce(logs,(prev, cur) =>  prev +'\n' + cur ,'')
            setLog(prev => `${prev}${appending}`)
        });

        return () => {
            ws?.close()
        }

    },[tokenId])

    return (
      <>
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
          <Typography variant="h4">토큰 버킷 알고리즘</Typography>
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
              sx={{ mt: 1, display: "flex", flexDirection: "column" }}
            >
              <Button
                sx={{ mt: 1 }}
                type="submit"
                variant="contained"
                color="primary"
              >
                수행
              </Button>
            </Box>
          </Box>

          <TextField
            sx={{ mt: 2, width: '80%' }}
            multiline
            rows={20}
            value={log}
            maxRows={20}
          />
        </Box>
      </>
    );
}

export default TokenBucketPage;