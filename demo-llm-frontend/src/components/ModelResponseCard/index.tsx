import { Card, CardContent, Typography, TextField } from '@mui/material';

interface ModelResponseCardProps {
  title: string;
  response: string;
}

export const ModelResponseCard: React.FC<ModelResponseCardProps> = ({ title, response }) => {
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <TextField
          multiline
          rows={8}
          fullWidth
          value={response}
          variant="outlined"
          InputProps={{
            readOnly: true,
          }}
        />
      </CardContent>
    </Card>
  );
}; 