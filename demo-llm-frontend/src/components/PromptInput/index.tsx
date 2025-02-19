import { TextField, Paper } from '@mui/material';

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
}

export const PromptInput: React.FC<PromptInputProps> = ({ value, onChange }) => {
  return (
    <Paper elevation={3} sx={{ p: 2, mb: 3 }}>
      <TextField
        fullWidth
        multiline
        rows={4}
        label="Enter your prompt (up to 8000 characters)"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        inputProps={{ maxLength: 8000 }}
        variant="outlined"
      />
    </Paper>
  );
}; 