export async function onRequest(context) {
  const { request } = context;
  
  // Handle CORS preflight requests
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      }
    });
  }
  
  // Handle feedback submission
  if (request.method === 'POST') {
    try {
      const formData = await request.json();
      const { page, rating, comment } = formData;
      
      // In a real implementation, this would store data in a database
      // For now, we'll just log it and return success
      
      console.log('Documentation feedback received:', { page, rating, comment });
      
      return new Response(
        JSON.stringify({ 
          success: true, 
          message: 'Feedback submitted successfully' 
        }),
        {
          headers: { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }
      );
    } catch (error) {
      return new Response(
        JSON.stringify({ 
          success: false, 
          message: 'Error processing feedback' 
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
  }
  
  // Handle feedback retrieval (GET request)
  if (request.method === 'GET') {
    // In a real implementation, this would retrieve data from a database
    return new Response(
      JSON.stringify({ 
        success: true, 
        data: [] 
      }),
      {
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
  
  return new Response('Method not allowed', { status: 405 });
}