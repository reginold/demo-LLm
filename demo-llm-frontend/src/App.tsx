import { useState } from 'react';
import { Container, Grid, Button, CircularProgress } from '@mui/material';
import { ModelResponseCard } from './components/ModelResponseCard';
import { PromptInput } from './components/PromptInput';
import { ModelService } from './services/api';
import { ComparisonState } from './types';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [responses, setResponses] = useState<ComparisonState>({
    llmJp172bResponse: 'Waiting for response...',
    gpt4oResponse: 'Waiting for response...',
    llama3405bResponse: 'Waiting for response...',
  });

  const handleCompare = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    try {
      const results = await ModelService.compareModels(prompt);
      setResponses(results);
    } catch (error) {
      console.error('Error comparing models:', error);
      setResponses({
        llmJp172bResponse: 'Error occurred while comparing models',
        gpt4oResponse: 'Error occurred while comparing models',
        llama3405bResponse: 'Error occurred while comparing models',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <h1>Model Comparison Demo</h1>
        
        <PromptInput value={prompt} onChange={setPrompt} />
        
        <Button
          variant="contained"
          onClick={handleCompare}
          disabled={loading || !prompt.trim()}
          sx={{ mb: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Compare Models'}
        </Button>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="LLM-JP-172B Model"
              response={responses.llmJp172bResponse}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="GPT-4o Model"
              response={responses.gpt4oResponse}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="Llama3-405B Model"
              response={responses.llama3405bResponse}
            />
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App; 