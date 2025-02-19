import { useState } from 'react';
import { Container, Grid, Button, CircularProgress, Typography, Box } from '@mui/material';
import { ModelResponseCard } from './components/ModelResponseCard';
import { PromptInput } from './components/PromptInput';
import { ModelService } from './services/api';
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

interface TimingInfo {
  duration: number;
}

interface ModelState {
  response: string;
  timing?: TimingInfo;
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [responses, setResponses] = useState<Record<string, ModelState>>({
    llmJp172bResponse: { response: '' },
    gpt4oResponse: { response: '' },
    llama3405bResponse: { response: '' },
  });

  const handleCompare = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setResponses({
      llmJp172bResponse: { response: '' },
      gpt4oResponse: { response: '' },
      llama3405bResponse: { response: '' },
    });

    try {
      await ModelService.compareModels(prompt, (modelId, content, timing) => {
        setResponses(prev => {
          const modelKey = {
            'llm_jp': 'llmJp172bResponse',
            'gpt4o': 'gpt4oResponse',
            'llama3': 'llama3405bResponse'
          }[modelId];

          if (!modelKey) return prev;

          return {
            ...prev,
            [modelKey]: {
              response: prev[modelKey].response + content,
              timing: timing || prev[modelKey].timing
            }
          };
        });
      });
    } catch (error) {
      console.error('Error comparing models:', error);
      const errorState = { response: 'Error occurred while comparing models' };
      setResponses({
        llmJp172bResponse: errorState,
        gpt4oResponse: errorState,
        llama3405bResponse: errorState,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 4, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Model Comparison Demo
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <PromptInput value={prompt} onChange={setPrompt} />
          
          <Button
            variant="contained"
            onClick={handleCompare}
            disabled={loading || !prompt.trim()}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Compare Models'}
          </Button>
        </Box>

        <Grid container spacing={3} sx={{ flex: 1 }}>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="LLM-JP-172B Model"
              response={responses.llmJp172bResponse.response}
              totalDuration={responses.llmJp172bResponse.timing?.duration}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="GPT-4o Model"
              response={responses.gpt4oResponse.response}
              totalDuration={responses.gpt4oResponse.timing?.duration}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ModelResponseCard
              title="Llama3-405B Model"
              response={responses.llama3405bResponse.response}
              totalDuration={responses.llama3405bResponse.timing?.duration}
            />
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App; 