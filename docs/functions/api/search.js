export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const limit = url.searchParams.get('limit') || 10;
  
  // Handle CORS preflight requests
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      }
    });
  }
  
  if (!query) {
    return new Response(
      JSON.stringify({ 
        success: false, 
        message: 'Query parameter "q" is required' 
      }),
      {
        status: 400,
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
  
  // In a real implementation, this would search through documentation content
  // For now, we'll return a mock response
  const mockResults = [
    {
      title: "Getting Started Guide",
      url: "/getting_started/index.html",
      excerpt: "Learn how to get started with LlamaIndex in just 5 lines of code...",
      score: 0.95
    },
    {
      title: "API Reference - Core Modules",
      url: "/api_reference/index.html",
      excerpt: "Complete API reference for LlamaIndex core modules...",
      score: 0.87
    },
    {
      title: "Example - RAG Pipeline",
      url: "/examples/rag_pipeline.html",
      excerpt: "Example implementation of a Retrieval-Augmented Generation pipeline...",
      score: 0.82
    }
  ];
  
  return new Response(
    JSON.stringify({ 
      success: true, 
      query: query,
      results: mockResults.slice(0, limit),
      total: mockResults.length
    }),
    {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }
  );
}