import { RayEventResponse, Response, request } from '@@/common/fetch';
import { AppBarComponent } from '@@/components/AppBar';
import { Label } from '@mui/icons-material';
import { AppBar, Box, Button, CircularProgress, FormControl, Input, InputLabel, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Toolbar, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import _ from 'lodash';
import dayjs from 'dayjs';

interface RateLimiterJobResult {
  name: string;
  start_time: Date;
  end_time: Date;
  result: {
    result: number[]
  }
}

const TokenBucketPage = () => {
    const [tokenId, setTokenId] = useState<string>('');
    const [log, setLog] = useState<string>('');
    const [isWorking, setIsWorking] = useState<boolean>(false);
    const [results, setResults] = useState<RateLimiterJobResult[]>();

    const columns = [
      '수행 ID',
      '요청 시간',
      '완료 시간',
      '성공 ( 200 )',
      '요청 거부 ( 429 )'
    ]

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
      (async ()=>{
        const { data } = (await request(
          "/rate_limiter" +
            "?domain=rate_limiter&sub_domain=token_bucket"
        )) as Response;
        setResults(data as RateLimiterJobResult[])
      })()

    },[])

    useEffect(()=>{
        setLog('')
        if (!tokenId) return;
        const baseUrl = window.location.hostname
        const ws = new WebSocket(
          `ws://${baseUrl}/api/v1/rate_limiter/status/token_bucket?id=${tokenId}`
        );
        setIsWorking(true);

        // Listen for messages
        ws.addEventListener('message', function (event) {
            // console.log(log);
            const result = JSON.parse(event.data) as RayEventResponse[];
            const logs = _.map(
              result,
              (item) =>
                `[${dayjs(parseInt(item.time)).format(
                  "YYYY-MM-DDTHH:mm:ss"
                )}] ` + `[${item.name}] [${item.status}] [${item.result}]`
            );

            // const g =
            //   /\[(?<time>\w+)\]\s\[(?<name>[\w\-]+)\]\s\[(?<status>\w+)\]\s\[(?<result>\w+)\]/;

            if (result[result.length-1].result == 'fin') {
              ws.close();
              setIsWorking(false);
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
              sx={{
                mt: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              {isWorking && <CircularProgress />}
              <Button
                sx={{ mt: 1 }}
                type="submit"
                variant="contained"
                color="primary"
                disabled={isWorking}
              >
                수행
              </Button>
            </Box>
          </Box>
          <Box
            sx={{
              alignItems: "center",
            }}
          >
            <TableContainer sx={{ alignItems: "center" }}>
              <Table sx={{ minWidth: 800 }}>
                <TableHead>
                  <TableRow>
                    {_.map(columns, (column) => (
                      <TableCell key={column}>{column}</TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {_.map(results, (item) => (
                    <TableRow>
                      <TableCell>{item.name}</TableCell>
                      <TableCell>
                        {dayjs(item.start_time).format("YYYY-MM-DDTHH:mm:ss")}
                      </TableCell>
                      <TableCell>
                        {dayjs(item.end_time).format("YYYY-MM-DDTHH:mm:ss")}
                      </TableCell>
                      <TableCell>
                        {item.result.result.filter(item => item == 200).length}
                      </TableCell>
                      <TableCell>
                        {item.result.result.filter(item => item == 429).length}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>

          <TextField
            sx={{ mt: 2, width: "80%" }}
            multiline
            rows={20}
            value={log}
          />
        </Box>
      </>
    );
}

export default TokenBucketPage;