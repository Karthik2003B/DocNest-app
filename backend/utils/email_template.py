def build_email_template(title, message, highlight=None):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:0; background-color:#0f172a; font-family:'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-image: url('http://googleusercontent.com/image_generation_content/0'); background-size: cover; background-position: center; background-repeat: no-repeat; padding: 60px 15px;">
            <tr>
                <td align="center">
                    <div style="max-width:650px; width:100%; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 24px; overflow: hidden; box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.1);">
                        
                        <div style="padding: 40px; text-align: center; background: linear-gradient(180deg, rgba(56, 189, 248, 0.08) 0%, rgba(255,255,255,0) 100%); border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <h1 style="margin: 0; font-size: 36px; font-weight: 800; background: linear-gradient(to right, #e0f2fe, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">DocNest</h1>
                            <p style="color: #94a3b8; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; margin: 12px 0 0 0;">Intelligent Document Ecosystem</p>
                        </div>
                        
                        <div style="padding: 45px 40px; background: rgba(255,255,255,0.01);">
                            <h2 style="color: #f8fafc; font-size: 24px; font-weight: 600; margin: 0 0 20px 0; letter-spacing: -0.5px;">{title}</h2>
                            
                            <p style="color: #cbd5e1; font-size: 16px; line-height: 1.8; margin: 0 0 32px 0;">
                                {message}
                            </p>
                            
                            {f'''
                            <div style="background: linear-gradient(90deg, rgba(56, 189, 248, 0.1) 0%, rgba(56, 189, 248, 0.0) 100%); border-left: 4px solid #38bdf8; padding: 20px 24px; border-radius: 0 12px 12px 0; margin-bottom: 35px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                                <strong style="color: #bae6fd; font-size: 16px; font-weight: 500; display: block; line-height: 1.5;">{highlight}</strong>
                            </div>
                            ''' if highlight else ''}
                            
                            <div style="text-align: center; margin-top: 10px;">
                                <a <a href="https://docnest.streamlit.app"> style="display: inline-block; padding: 16px 36px; background: linear-gradient(135deg, #0284c7 0%, #3b82f6 100%); color: #ffffff; font-size: 16px; font-weight: 600; text-decoration: none; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.5), inset 0 1px 0 rgba(255,255,255,0.2); text-transform: uppercase; letter-spacing: 1px;">
                                    Access Workspace
                                </a>
                            </div>
                        </div>
                        
                        <div style="padding: 30px 40px; text-align: center; background: rgba(0,0,0,0.4); border-top: 1px solid rgba(255,255,255,0.05);">
                            <p style="color: #64748b; font-size: 12px; margin: 0; line-height: 1.6;">
                                Secure, automated transmission from DocNest Core.<br>
                                © 2026 DocNest Intelligence. All rights reserved.
                            </p>
                        </div>
                        
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """