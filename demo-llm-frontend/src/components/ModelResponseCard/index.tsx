import React, { useRef, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Stack } from '@mui/material';

interface ModelResponseCardProps {
  title: string;
  response: string;
  totalDuration?: number;
}

export const ModelResponseCard: React.FC<ModelResponseCardProps> = ({ 
  title, 
  response, 
  totalDuration 
}) => {
  const responseRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (responseRef.current) {
      responseRef.current.scrollTop = responseRef.current.scrollHeight;
    }
  }, [response]);

  // Convert milliseconds to seconds
  const formatDuration = (ms?: number) => {
    if (ms === undefined) return undefined;
    return (ms / 1000).toFixed(2);
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flex: '0 0 auto', pb: 1 }}>
        <Stack spacing={1}>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
          {totalDuration !== undefined && (
            <Typography variant="caption" sx={{ fontFamily: 'monospace', opacity: 0.7 }}>
              Duration: {formatDuration(totalDuration)}s
            </Typography>
          )}
        </Stack>
      </CardContent>
      <Box
        ref={responseRef}
        sx={{
          flex: '1 1 auto',
          overflowY: 'auto',
          maxHeight: '60vh',
          minHeight: '60vh',
          p: 2,
          backgroundColor: 'rgba(0, 0, 0, 0.1)',
          fontFamily: 'monospace',
          whiteSpace: 'pre-wrap',
          '&::-webkit-scrollbar': {
            width: '8px',
          },
          '&::-webkit-scrollbar-track': {
            background: 'rgba(0, 0, 0, 0.1)',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'rgba(255, 255, 255, 0.3)',
            borderRadius: '4px',
          },
          '&::-webkit-scrollbar-thumb:hover': {
            background: 'rgba(255, 255, 255, 0.4)',
          },
        }}
      >
        {response || 'Waiting for response...'}
      </Box>
    </Card>
  );
};