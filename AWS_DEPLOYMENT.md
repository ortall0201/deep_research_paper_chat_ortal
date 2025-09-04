# AWS Deployment Guide - CrewAI Research Application

## 🚀 **Deploy to AWS App Runner (LinkedIn-Worthy!)**

### **Prerequisites**
- AWS Account ([Create one free](https://aws.amazon.com/free/))
- Your Docker image built via GitHub Actions: `ghcr.io/ortall0201/deep_research_paper_chat_ortal:latest`

### **Step 1: Setup AWS CLI (Optional but Professional)**
```bash
# Install AWS CLI
pip install awscli

# Configure with your credentials
aws configure
```

### **Step 2: Deploy via AWS Console (Easiest)**

1. **Go to AWS App Runner Console**
   - Visit: https://console.aws.amazon.com/apprunner/
   - Click "Create service"

2. **Configure Source**
   - **Source type**: Container registry
   - **Provider**: GitHub Container Registry
   - **Container image URI**: `ghcr.io/ortall0201/deep_research_paper_chat_ortal:latest`
   - **Deployment trigger**: Manual (or Automatic for CI/CD)

3. **Configure Service**
   - **Service name**: `crewai-research-app`
   - **Virtual CPU**: 0.25 vCPU
   - **Memory**: 0.5 GB
   - **Port**: 8000

4. **Environment Variables** (Add these)
   ```
   OPENAI_API_KEY=your_openai_key_here
   FIRECRAWL_API_KEY=your_firecrawl_key_here
   ENVIRONMENT=production
   PORT=8000
   ```

5. **Auto Scaling**
   - **Min instances**: 1
   - **Max instances**: 10
   - **Max concurrency**: 100

6. **Health Check**
   - **Path**: `/health`
   - **Interval**: 20 seconds
   - **Timeout**: 5 seconds
   - **Healthy threshold**: 3
   - **Unhealthy threshold**: 3

### **Step 3: Deploy & Test**

1. **Click "Create and Deploy"** 
2. **Wait 5-10 minutes** for deployment
3. **Get your URL**: `https://your-app-id.region.awsapprunner.com`
4. **Test the endpoints**:
   - Frontend: `https://your-url.com` (port 3000 internally)
   - Backend API: `https://your-url.com` (port 8000)
   - Health check: `https://your-url.com/health`

### **Step 4: Custom Domain (Optional LinkedIn Flex)**

1. **Go to App Runner → Custom domains**
2. **Add your domain** (requires domain ownership verification)
3. **Configure DNS** with provided CNAME records
4. **SSL certificate** automatically provisioned

### **💰 Expected Costs**
- **Base cost**: ~$12/month (0.25 vCPU + 0.5GB RAM)
- **Data transfer**: First 1GB free, then $0.09/GB
- **Scaling**: Pay only for what you use

### **🔒 Security Features**
- ✅ **HTTPS by default** with managed SSL certificates
- ✅ **Private networking** with VPC integration available
- ✅ **IAM integration** for secure access
- ✅ **CloudWatch monitoring** included
- ✅ **AWS WAF** integration available

### **📊 Monitoring & Logs**
- **CloudWatch Logs**: Automatic log collection
- **Metrics**: CPU, Memory, Request count, Response time
- **Alarms**: Set up alerts for high error rates or latency

### **🚀 LinkedIn Post Template**
```
🔥 Just deployed my AI-powered research application on AWS! 

Architecture highlights:
✅ Containerized with Docker multi-stage builds
✅ Deployed on AWS App Runner with auto-scaling
✅ CI/CD pipeline with GitHub Actions
✅ Full-stack: React frontend + FastAPI backend
✅ AI integration with CrewAI for intelligent research
✅ Production monitoring with CloudWatch
✅ HTTPS with managed SSL certificates

The app performs intelligent intent classification and conducts comprehensive academic research using multiple AI agents. Pretty excited about this cloud-native architecture!

Tech stack: #AWS #Docker #Python #React #AI #CrewAI #CloudNative #DevOps

Live demo: https://your-app.awsapprunner.com
```

### **🔄 Continuous Deployment (Pro Level)**

To enable automatic deployment when you push to GitHub:

1. **In App Runner Console**:
   - Edit service → Source
   - Enable "Automatic deployments"
   - Configure webhook URL in GitHub

2. **GitHub Container Registry Integration**:
   - App Runner watches for new image tags
   - Automatically deploys latest version
   - Zero downtime deployments

### **⚡ Advanced: ECS Fargate Upgrade Path**

When you're ready for more complex architecture:
- **ECS Fargate**: Container orchestration
- **Application Load Balancer**: Advanced routing
- **RDS**: Managed database
- **ElastiCache**: Redis caching
- **CloudFront**: Global CDN

### **🛠️ Troubleshooting**

**Build fails?**
- Check Docker image is public or configure ECR access
- Verify environment variables are set
- Check CloudWatch logs for errors

**Health check failing?**
- Ensure `/health` endpoint returns 200 OK
- Check port configuration (8000)
- Verify app starts within 4 minutes

**High costs?**
- Reduce instance size (0.25 vCPU, 0.5GB RAM)
- Enable auto-pause for dev environments
- Monitor data transfer costs

### **🎯 Next Steps**

1. **Deploy your app** using the steps above
2. **Monitor performance** in CloudWatch
3. **Share on LinkedIn** with the template above
4. **Consider upgrades**: Custom domain, ECS Fargate, or additional AWS services

**Ready to become an AWS cloud architect?** 🌟

---

**Total deployment time**: ~15 minutes  
**Monthly cost**: ~$12  
**LinkedIn impressions**: Priceless 😎