# Cloudflare Pages Deployment for LlamaIndex Documentation

This directory contains the configuration and scripts needed to deploy the LlamaIndex documentation to Cloudflare Pages.

## Deployment Process

The documentation is automatically built and deployed to Cloudflare Pages using the following process:

1. **Build Script**: `build-cloudflare.sh` handles the complete build process
2. **Configuration**: `wrangler.toml` defines the Cloudflare Pages configuration
3. **Functions**: Serverless functions in the `functions/` directory provide dynamic capabilities

## Cloudflare Pages Functions

This deployment includes serverless functions that enhance the documentation experience:

- `/api/feedback` - Collects user feedback on documentation pages
- `/api/search` - Provides API reference search functionality

## Advanced Features

Beyond static hosting, Cloudflare Pages offers several advanced features:

1. **Serverless Functions**: Execute code at the edge without managing servers
2. **Global Network**: Leverage Cloudflare's worldwide edge locations for low-latency delivery
3. **Integration with Cloudflare Services**: 
   - R2 Storage for large documentation assets
   - D1 Database for analytics and user data
   - Workers for more complex serverless logic

See `cloudflare_advanced_features.md` for detailed proposals on leveraging these capabilities.

## Local Development

To test the Cloudflare Pages deployment locally:

1. Install Wrangler: `npm install -g wrangler`
2. Run the build script: `./build-cloudflare.sh`
3. Start the local server: `wrangler pages dev dist`

## Deployment

The documentation is automatically deployed to Cloudflare Pages on every push to the main branch through GitHub Actions.